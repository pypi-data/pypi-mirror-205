from __future__ import annotations

from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING, Any, Dict
from uuid import UUID

from sqlalchemy.orm import Session

from xcnt.drivr.metadata_client.enum import DataTypeEnum
from xcnt.drivr.metadata_client.lookup import MetadataLookup
from xcnt.drivr.metadata_client.model import MetadataType
from xcnt.drivr.metadata_client.model.metadata_field import InstantiatedMetadataField

if TYPE_CHECKING:
    from xcnt.drivr.metadata_client.command.metadata_value_command import MetadataValueCommand


expected_python_types = {
    DataTypeEnum.BOOLEAN: bool,
    DataTypeEnum.FLOAT: float,
    DataTypeEnum.INTEGER: int,
    DataTypeEnum.STRING: str,
    DataTypeEnum.TIMESTAMP: datetime,
    DataTypeEnum.UUID: UUID,
    #########################################################################
    #                                                                       #
    #  CAUTION:                                                             #
    #  Commented out until document and image are fully supported by DRIVR  #
    #                                                                       #
    #########################################################################
    # DataTypeEnum.DOCUMENT: UUID,
    # DataTypeEnum.IMAGE: UUID,
}


expected_python_type_converter = {DataTypeEnum.TIMESTAMP: datetime.fromisoformat}


class MetadataValidationChecker:
    command: MetadataValueCommand

    def __init__(self, command: MetadataValueCommand):
        self.command = command
        self._lookup = MetadataLookup(
            session=self.command.session,
            entity_type=self.command.metadata_entity_type,
            domain_uuid=self.command.metadata_domain_uuid,
            entity_uuid=self.command.aggregate_id,
        )

    @property
    def entity_uuid(self) -> UUID:
        return self.command.aggregate_id

    @property
    def session(self) -> Session:
        return self.command.session

    @property
    def type_dict(self) -> Dict[str, MetadataType]:
        return self._lookup.types

    @property
    def existing_value_dict(self) -> Dict[str, Any]:
        return self._lookup.values

    @property
    def to_set_dict(self) -> Dict[str, Any]:
        metadata = getattr(self.command, "metadata", None)
        if not metadata:
            return {}
        if isinstance(metadata, InstantiatedMetadataField):
            return metadata._to_dict()
        return metadata

    @cached_property
    def to_check_dict(self) -> Dict[str, Any]:
        return {**self.existing_value_dict, **self.to_set_dict}

    def get_validation_errors(self) -> Dict[str, str]:
        messages = {}
        for key, metadata_type in self.type_dict.items():
            error_messages = self._validate_for_type(metadata_type)
            for sub_key, error_message in error_messages.items():
                messages[f"metadata.{key}.{sub_key}"] = error_message
        return messages

    def _validate_for_type(self, metadata_type: MetadataType) -> Dict[str, str]:
        error_messages: Dict[str, str] = {}
        if self._has_not_null_error(metadata_type):
            error_messages["not_null"] = "Field must not be None"

        value = self.to_check_dict.get(metadata_type.key, None)
        if self._has_unique_error(metadata_type):
            error_messages["unique"] = f'The value "{value}" in "{metadata_type.key}" already exists'

        if self._is_correct_type_error(metadata_type):
            error_messages[
                "type_mismatch"
            ] = f'The value "{value}" could not be converted to the type "{metadata_type.data_type.value}"'

        return error_messages

    def _has_not_null_error(self, metadata_type: MetadataType) -> bool:
        if metadata_type.mandatory and metadata_type.default_value is None:
            if self.to_check_dict.get(metadata_type.key, None) is None:
                return True

        return False

    def _has_unique_error(self, metadata_type: MetadataType) -> bool:
        value = self.to_check_dict.get(str(metadata_type.key), None)
        if not metadata_type.unique or value is None:
            return False

        metadata_value_class = self._lookup.metadata_value_class
        metadata_value_lookup_class = self._lookup.metadata_value_lookup_class

        query = (
            self.session.query(metadata_value_lookup_class)
            .join(
                metadata_value_class,
                metadata_value_lookup_class.metadata_value_uuid == metadata_value_class.uuid,
                isouter=True,
            )
            .where(
                metadata_value_lookup_class.metadata_type_uuid == metadata_type.uuid,
                getattr(metadata_value_class, metadata_value_class.value_column_name_for(metadata_type.data_type))
                == value,
            )
            .filter(
                metadata_value_lookup_class.entity_uuid != self.entity_uuid,
            )
        )

        return query.count() > 0

    def _is_correct_type_error(self, metadata_type: MetadataType) -> bool:
        value = self.to_check_dict.get(metadata_type.key, None)
        if value is None:
            return False

        expected_type = expected_python_types[metadata_type.data_type]
        if not isinstance(value, expected_type):
            converter = expected_python_type_converter.get(metadata_type.data_type, expected_type)
            try:
                value = converter(value)
            except ValueError:
                pass

            self.to_set_dict[metadata_type.key] = value

        return not isinstance(value, expected_type)
