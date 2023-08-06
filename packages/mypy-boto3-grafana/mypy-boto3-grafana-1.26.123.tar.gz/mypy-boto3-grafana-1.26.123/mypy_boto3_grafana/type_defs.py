"""
Type annotations for grafana service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/type_defs/)

Usage::

    ```python
    from mypy_boto3_grafana.type_defs import AssertionAttributesTypeDef

    data: AssertionAttributesTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AccountAccessTypeType,
    AuthenticationProviderTypesType,
    DataSourceTypeType,
    LicenseTypeType,
    PermissionTypeType,
    RoleType,
    SamlConfigurationStatusType,
    UpdateActionType,
    UserTypeType,
    WorkspaceStatusType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AssertionAttributesTypeDef",
    "AssociateLicenseRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AwsSsoAuthenticationTypeDef",
    "AuthenticationSummaryTypeDef",
    "CreateWorkspaceApiKeyRequestRequestTypeDef",
    "NetworkAccessConfigurationTypeDef",
    "VpcConfigurationTypeDef",
    "DeleteWorkspaceApiKeyRequestRequestTypeDef",
    "DeleteWorkspaceRequestRequestTypeDef",
    "DescribeWorkspaceAuthenticationRequestRequestTypeDef",
    "DescribeWorkspaceConfigurationRequestRequestTypeDef",
    "DescribeWorkspaceRequestRequestTypeDef",
    "DisassociateLicenseRequestRequestTypeDef",
    "IdpMetadataTypeDef",
    "PaginatorConfigTypeDef",
    "ListPermissionsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWorkspacesRequestRequestTypeDef",
    "UserTypeDef",
    "RoleValuesTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateWorkspaceConfigurationRequestRequestTypeDef",
    "CreateWorkspaceApiKeyResponseTypeDef",
    "DeleteWorkspaceApiKeyResponseTypeDef",
    "DescribeWorkspaceConfigurationResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "WorkspaceSummaryTypeDef",
    "CreateWorkspaceRequestRequestTypeDef",
    "UpdateWorkspaceRequestRequestTypeDef",
    "WorkspaceDescriptionTypeDef",
    "ListPermissionsRequestListPermissionsPaginateTypeDef",
    "ListWorkspacesRequestListWorkspacesPaginateTypeDef",
    "PermissionEntryTypeDef",
    "UpdateInstructionTypeDef",
    "SamlConfigurationTypeDef",
    "ListWorkspacesResponseTypeDef",
    "AssociateLicenseResponseTypeDef",
    "CreateWorkspaceResponseTypeDef",
    "DeleteWorkspaceResponseTypeDef",
    "DescribeWorkspaceResponseTypeDef",
    "DisassociateLicenseResponseTypeDef",
    "UpdateWorkspaceResponseTypeDef",
    "ListPermissionsResponseTypeDef",
    "UpdateErrorTypeDef",
    "UpdatePermissionsRequestRequestTypeDef",
    "SamlAuthenticationTypeDef",
    "UpdateWorkspaceAuthenticationRequestRequestTypeDef",
    "UpdatePermissionsResponseTypeDef",
    "AuthenticationDescriptionTypeDef",
    "DescribeWorkspaceAuthenticationResponseTypeDef",
    "UpdateWorkspaceAuthenticationResponseTypeDef",
)

AssertionAttributesTypeDef = TypedDict(
    "AssertionAttributesTypeDef",
    {
        "email": str,
        "groups": str,
        "login": str,
        "name": str,
        "org": str,
        "role": str,
    },
    total=False,
)

AssociateLicenseRequestRequestTypeDef = TypedDict(
    "AssociateLicenseRequestRequestTypeDef",
    {
        "licenseType": LicenseTypeType,
        "workspaceId": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

AwsSsoAuthenticationTypeDef = TypedDict(
    "AwsSsoAuthenticationTypeDef",
    {
        "ssoClientId": str,
    },
    total=False,
)

_RequiredAuthenticationSummaryTypeDef = TypedDict(
    "_RequiredAuthenticationSummaryTypeDef",
    {
        "providers": List[AuthenticationProviderTypesType],
    },
)
_OptionalAuthenticationSummaryTypeDef = TypedDict(
    "_OptionalAuthenticationSummaryTypeDef",
    {
        "samlConfigurationStatus": SamlConfigurationStatusType,
    },
    total=False,
)


class AuthenticationSummaryTypeDef(
    _RequiredAuthenticationSummaryTypeDef, _OptionalAuthenticationSummaryTypeDef
):
    pass


CreateWorkspaceApiKeyRequestRequestTypeDef = TypedDict(
    "CreateWorkspaceApiKeyRequestRequestTypeDef",
    {
        "keyName": str,
        "keyRole": str,
        "secondsToLive": int,
        "workspaceId": str,
    },
)

NetworkAccessConfigurationTypeDef = TypedDict(
    "NetworkAccessConfigurationTypeDef",
    {
        "prefixListIds": List[str],
        "vpceIds": List[str],
    },
)

VpcConfigurationTypeDef = TypedDict(
    "VpcConfigurationTypeDef",
    {
        "securityGroupIds": List[str],
        "subnetIds": List[str],
    },
)

DeleteWorkspaceApiKeyRequestRequestTypeDef = TypedDict(
    "DeleteWorkspaceApiKeyRequestRequestTypeDef",
    {
        "keyName": str,
        "workspaceId": str,
    },
)

DeleteWorkspaceRequestRequestTypeDef = TypedDict(
    "DeleteWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)

DescribeWorkspaceAuthenticationRequestRequestTypeDef = TypedDict(
    "DescribeWorkspaceAuthenticationRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)

DescribeWorkspaceConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeWorkspaceConfigurationRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)

DescribeWorkspaceRequestRequestTypeDef = TypedDict(
    "DescribeWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)

DisassociateLicenseRequestRequestTypeDef = TypedDict(
    "DisassociateLicenseRequestRequestTypeDef",
    {
        "licenseType": LicenseTypeType,
        "workspaceId": str,
    },
)

IdpMetadataTypeDef = TypedDict(
    "IdpMetadataTypeDef",
    {
        "url": str,
        "xml": str,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredListPermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredListPermissionsRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalListPermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalListPermissionsRequestRequestTypeDef",
    {
        "groupId": str,
        "maxResults": int,
        "nextToken": str,
        "userId": str,
        "userType": UserTypeType,
    },
    total=False,
)


class ListPermissionsRequestRequestTypeDef(
    _RequiredListPermissionsRequestRequestTypeDef, _OptionalListPermissionsRequestRequestTypeDef
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListWorkspacesRequestRequestTypeDef = TypedDict(
    "ListWorkspacesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "id": str,
        "type": UserTypeType,
    },
)

RoleValuesTypeDef = TypedDict(
    "RoleValuesTypeDef",
    {
        "admin": List[str],
        "editor": List[str],
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UpdateWorkspaceConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateWorkspaceConfigurationRequestRequestTypeDef",
    {
        "configuration": str,
        "workspaceId": str,
    },
)

CreateWorkspaceApiKeyResponseTypeDef = TypedDict(
    "CreateWorkspaceApiKeyResponseTypeDef",
    {
        "key": str,
        "keyName": str,
        "workspaceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteWorkspaceApiKeyResponseTypeDef = TypedDict(
    "DeleteWorkspaceApiKeyResponseTypeDef",
    {
        "keyName": str,
        "workspaceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorkspaceConfigurationResponseTypeDef = TypedDict(
    "DescribeWorkspaceConfigurationResponseTypeDef",
    {
        "configuration": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredWorkspaceSummaryTypeDef = TypedDict(
    "_RequiredWorkspaceSummaryTypeDef",
    {
        "authentication": AuthenticationSummaryTypeDef,
        "created": datetime,
        "endpoint": str,
        "grafanaVersion": str,
        "id": str,
        "modified": datetime,
        "status": WorkspaceStatusType,
    },
)
_OptionalWorkspaceSummaryTypeDef = TypedDict(
    "_OptionalWorkspaceSummaryTypeDef",
    {
        "description": str,
        "name": str,
        "notificationDestinations": List[Literal["SNS"]],
        "tags": Dict[str, str],
    },
    total=False,
)


class WorkspaceSummaryTypeDef(_RequiredWorkspaceSummaryTypeDef, _OptionalWorkspaceSummaryTypeDef):
    pass


_RequiredCreateWorkspaceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWorkspaceRequestRequestTypeDef",
    {
        "accountAccessType": AccountAccessTypeType,
        "authenticationProviders": Sequence[AuthenticationProviderTypesType],
        "permissionType": PermissionTypeType,
    },
)
_OptionalCreateWorkspaceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWorkspaceRequestRequestTypeDef",
    {
        "clientToken": str,
        "configuration": str,
        "grafanaVersion": str,
        "networkAccessControl": NetworkAccessConfigurationTypeDef,
        "organizationRoleName": str,
        "stackSetName": str,
        "tags": Mapping[str, str],
        "vpcConfiguration": VpcConfigurationTypeDef,
        "workspaceDataSources": Sequence[DataSourceTypeType],
        "workspaceDescription": str,
        "workspaceName": str,
        "workspaceNotificationDestinations": Sequence[Literal["SNS"]],
        "workspaceOrganizationalUnits": Sequence[str],
        "workspaceRoleArn": str,
    },
    total=False,
)


class CreateWorkspaceRequestRequestTypeDef(
    _RequiredCreateWorkspaceRequestRequestTypeDef, _OptionalCreateWorkspaceRequestRequestTypeDef
):
    pass


_RequiredUpdateWorkspaceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalUpdateWorkspaceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWorkspaceRequestRequestTypeDef",
    {
        "accountAccessType": AccountAccessTypeType,
        "networkAccessControl": NetworkAccessConfigurationTypeDef,
        "organizationRoleName": str,
        "permissionType": PermissionTypeType,
        "removeNetworkAccessConfiguration": bool,
        "removeVpcConfiguration": bool,
        "stackSetName": str,
        "vpcConfiguration": VpcConfigurationTypeDef,
        "workspaceDataSources": Sequence[DataSourceTypeType],
        "workspaceDescription": str,
        "workspaceName": str,
        "workspaceNotificationDestinations": Sequence[Literal["SNS"]],
        "workspaceOrganizationalUnits": Sequence[str],
        "workspaceRoleArn": str,
    },
    total=False,
)


class UpdateWorkspaceRequestRequestTypeDef(
    _RequiredUpdateWorkspaceRequestRequestTypeDef, _OptionalUpdateWorkspaceRequestRequestTypeDef
):
    pass


_RequiredWorkspaceDescriptionTypeDef = TypedDict(
    "_RequiredWorkspaceDescriptionTypeDef",
    {
        "authentication": AuthenticationSummaryTypeDef,
        "created": datetime,
        "dataSources": List[DataSourceTypeType],
        "endpoint": str,
        "grafanaVersion": str,
        "id": str,
        "modified": datetime,
        "status": WorkspaceStatusType,
    },
)
_OptionalWorkspaceDescriptionTypeDef = TypedDict(
    "_OptionalWorkspaceDescriptionTypeDef",
    {
        "accountAccessType": AccountAccessTypeType,
        "description": str,
        "freeTrialConsumed": bool,
        "freeTrialExpiration": datetime,
        "licenseExpiration": datetime,
        "licenseType": LicenseTypeType,
        "name": str,
        "networkAccessControl": NetworkAccessConfigurationTypeDef,
        "notificationDestinations": List[Literal["SNS"]],
        "organizationRoleName": str,
        "organizationalUnits": List[str],
        "permissionType": PermissionTypeType,
        "stackSetName": str,
        "tags": Dict[str, str],
        "vpcConfiguration": VpcConfigurationTypeDef,
        "workspaceRoleArn": str,
    },
    total=False,
)


class WorkspaceDescriptionTypeDef(
    _RequiredWorkspaceDescriptionTypeDef, _OptionalWorkspaceDescriptionTypeDef
):
    pass


_RequiredListPermissionsRequestListPermissionsPaginateTypeDef = TypedDict(
    "_RequiredListPermissionsRequestListPermissionsPaginateTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalListPermissionsRequestListPermissionsPaginateTypeDef = TypedDict(
    "_OptionalListPermissionsRequestListPermissionsPaginateTypeDef",
    {
        "groupId": str,
        "userId": str,
        "userType": UserTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListPermissionsRequestListPermissionsPaginateTypeDef(
    _RequiredListPermissionsRequestListPermissionsPaginateTypeDef,
    _OptionalListPermissionsRequestListPermissionsPaginateTypeDef,
):
    pass


ListWorkspacesRequestListWorkspacesPaginateTypeDef = TypedDict(
    "ListWorkspacesRequestListWorkspacesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

PermissionEntryTypeDef = TypedDict(
    "PermissionEntryTypeDef",
    {
        "role": RoleType,
        "user": UserTypeDef,
    },
)

UpdateInstructionTypeDef = TypedDict(
    "UpdateInstructionTypeDef",
    {
        "action": UpdateActionType,
        "role": RoleType,
        "users": Sequence[UserTypeDef],
    },
)

_RequiredSamlConfigurationTypeDef = TypedDict(
    "_RequiredSamlConfigurationTypeDef",
    {
        "idpMetadata": IdpMetadataTypeDef,
    },
)
_OptionalSamlConfigurationTypeDef = TypedDict(
    "_OptionalSamlConfigurationTypeDef",
    {
        "allowedOrganizations": List[str],
        "assertionAttributes": AssertionAttributesTypeDef,
        "loginValidityDuration": int,
        "roleValues": RoleValuesTypeDef,
    },
    total=False,
)


class SamlConfigurationTypeDef(
    _RequiredSamlConfigurationTypeDef, _OptionalSamlConfigurationTypeDef
):
    pass


ListWorkspacesResponseTypeDef = TypedDict(
    "ListWorkspacesResponseTypeDef",
    {
        "nextToken": str,
        "workspaces": List[WorkspaceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateLicenseResponseTypeDef = TypedDict(
    "AssociateLicenseResponseTypeDef",
    {
        "workspace": WorkspaceDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateWorkspaceResponseTypeDef = TypedDict(
    "CreateWorkspaceResponseTypeDef",
    {
        "workspace": WorkspaceDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteWorkspaceResponseTypeDef = TypedDict(
    "DeleteWorkspaceResponseTypeDef",
    {
        "workspace": WorkspaceDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorkspaceResponseTypeDef = TypedDict(
    "DescribeWorkspaceResponseTypeDef",
    {
        "workspace": WorkspaceDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateLicenseResponseTypeDef = TypedDict(
    "DisassociateLicenseResponseTypeDef",
    {
        "workspace": WorkspaceDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateWorkspaceResponseTypeDef = TypedDict(
    "UpdateWorkspaceResponseTypeDef",
    {
        "workspace": WorkspaceDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPermissionsResponseTypeDef = TypedDict(
    "ListPermissionsResponseTypeDef",
    {
        "nextToken": str,
        "permissions": List[PermissionEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateErrorTypeDef = TypedDict(
    "UpdateErrorTypeDef",
    {
        "causedBy": UpdateInstructionTypeDef,
        "code": int,
        "message": str,
    },
)

UpdatePermissionsRequestRequestTypeDef = TypedDict(
    "UpdatePermissionsRequestRequestTypeDef",
    {
        "updateInstructionBatch": Sequence[UpdateInstructionTypeDef],
        "workspaceId": str,
    },
)

_RequiredSamlAuthenticationTypeDef = TypedDict(
    "_RequiredSamlAuthenticationTypeDef",
    {
        "status": SamlConfigurationStatusType,
    },
)
_OptionalSamlAuthenticationTypeDef = TypedDict(
    "_OptionalSamlAuthenticationTypeDef",
    {
        "configuration": SamlConfigurationTypeDef,
    },
    total=False,
)


class SamlAuthenticationTypeDef(
    _RequiredSamlAuthenticationTypeDef, _OptionalSamlAuthenticationTypeDef
):
    pass


_RequiredUpdateWorkspaceAuthenticationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWorkspaceAuthenticationRequestRequestTypeDef",
    {
        "authenticationProviders": Sequence[AuthenticationProviderTypesType],
        "workspaceId": str,
    },
)
_OptionalUpdateWorkspaceAuthenticationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWorkspaceAuthenticationRequestRequestTypeDef",
    {
        "samlConfiguration": SamlConfigurationTypeDef,
    },
    total=False,
)


class UpdateWorkspaceAuthenticationRequestRequestTypeDef(
    _RequiredUpdateWorkspaceAuthenticationRequestRequestTypeDef,
    _OptionalUpdateWorkspaceAuthenticationRequestRequestTypeDef,
):
    pass


UpdatePermissionsResponseTypeDef = TypedDict(
    "UpdatePermissionsResponseTypeDef",
    {
        "errors": List[UpdateErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAuthenticationDescriptionTypeDef = TypedDict(
    "_RequiredAuthenticationDescriptionTypeDef",
    {
        "providers": List[AuthenticationProviderTypesType],
    },
)
_OptionalAuthenticationDescriptionTypeDef = TypedDict(
    "_OptionalAuthenticationDescriptionTypeDef",
    {
        "awsSso": AwsSsoAuthenticationTypeDef,
        "saml": SamlAuthenticationTypeDef,
    },
    total=False,
)


class AuthenticationDescriptionTypeDef(
    _RequiredAuthenticationDescriptionTypeDef, _OptionalAuthenticationDescriptionTypeDef
):
    pass


DescribeWorkspaceAuthenticationResponseTypeDef = TypedDict(
    "DescribeWorkspaceAuthenticationResponseTypeDef",
    {
        "authentication": AuthenticationDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateWorkspaceAuthenticationResponseTypeDef = TypedDict(
    "UpdateWorkspaceAuthenticationResponseTypeDef",
    {
        "authentication": AuthenticationDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
