from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Type

from xcnt.cqrs.command.validations import Validator

from xcnt.drivr.metadata_client.command.validation.metadata_validation_checker import MetadataValidationChecker

if TYPE_CHECKING:
    from xcnt.drivr.metadata_client.command.metadata_value_command import MetadataValueCommand


class MetadataValidator(Validator):
    command: MetadataValueCommand
    command_class: Type[MetadataValueCommand]

    def get_validation_errors(self) -> Dict[str, str]:
        errors = super().get_validation_errors()
        errors.update(self._get_metadata_validation_errors())
        return errors

    def _get_metadata_validation_errors(self) -> Dict[str, str]:
        checker = MetadataValidationChecker(self.command)
        return checker.get_validation_errors()
