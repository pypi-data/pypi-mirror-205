from marshmallow import fields

from xcnt.drivr.metadata_client.enum import DataTypeEnum

TYPE_FIELD_LOOKUP = {
    DataTypeEnum.BOOLEAN: fields.Boolean,
    DataTypeEnum.FLOAT: fields.Float,
    DataTypeEnum.INTEGER: fields.Integer,
    DataTypeEnum.STRING: fields.String,
    DataTypeEnum.TIMESTAMP: fields.DateTime,
    DataTypeEnum.UUID: fields.UUID,
    #########################################################################
    #                                                                       #
    #  CAUTION:                                                             #
    #  Commented out until document and image are fully supported by DRIVR  #
    #                                                                       #
    #########################################################################
    # DataTypeEnum.DOCUMENT: fields.UUID,
    # DataTypeEnum.IMAGE: fields.UUID,
}

DATA_TYPE_INPUT_FIELD_MAPPING = {
    DataTypeEnum.BOOLEAN: "boolean",
    DataTypeEnum.FLOAT: "float",
    DataTypeEnum.INTEGER: "integer",
    DataTypeEnum.STRING: "string",
    DataTypeEnum.TIMESTAMP: "timestamp",
    DataTypeEnum.UUID: "uuid",
    #########################################################################
    #                                                                       #
    #  CAUTION:                                                             #
    #  Commented out until document and image are fully supported by DRIVR  #
    #                                                                       #
    #########################################################################
    # DataTypeEnum.DOCUMENT: "document",
    # DataTypeEnum.IMAGE: "image",
}
