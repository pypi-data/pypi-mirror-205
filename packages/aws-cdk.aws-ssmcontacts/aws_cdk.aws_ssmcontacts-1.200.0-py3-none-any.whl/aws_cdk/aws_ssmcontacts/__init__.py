'''
# AWS::SSMContacts Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_ssmcontacts as ssmcontacts
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for SSMContacts construct libraries](https://constructs.dev/search?q=ssmcontacts)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::SSMContacts resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SSMContacts.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::SSMContacts](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SSMContacts.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnContact(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssmcontacts.CfnContact",
):
    '''A CloudFormation ``AWS::SSMContacts::Contact``.

    The ``AWS::SSMContacts::Contact`` resource specifies a contact or escalation plan. Incident Manager contacts are a subset of actions and data types that you can use for managing responder engagement and interaction.

    :cloudformationResource: AWS::SSMContacts::Contact
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ssmcontacts as ssmcontacts
        
        cfn_contact = ssmcontacts.CfnContact(self, "MyCfnContact",
            alias="alias",
            display_name="displayName",
            type="type",
        
            # the properties below are optional
            plan=[ssmcontacts.CfnContact.StageProperty(
                duration_in_minutes=123,
        
                # the properties below are optional
                targets=[ssmcontacts.CfnContact.TargetsProperty(
                    channel_target_info=ssmcontacts.CfnContact.ChannelTargetInfoProperty(
                        channel_id="channelId",
                        retry_interval_in_minutes=123
                    ),
                    contact_target_info=ssmcontacts.CfnContact.ContactTargetInfoProperty(
                        contact_id="contactId",
                        is_essential=False
                    )
                )]
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        alias: builtins.str,
        display_name: builtins.str,
        type: builtins.str,
        plan: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnContact.StageProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    ) -> None:
        '''Create a new ``AWS::SSMContacts::Contact``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param alias: The unique and identifiable alias of the contact or escalation plan.
        :param display_name: The full name of the contact or escalation plan.
        :param type: Refers to the type of contact:. - ``PERSONAL`` : A single, individual contact. - ``ESCALATION`` : An escalation plan. - ``ONCALL_SCHEDULE`` : An on-call schedule.
        :param plan: A list of stages. A contact has an engagement plan with stages that contact specified contact channels. An escalation plan uses stages that contact specified contacts.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6ca3ad36cfd3d6487f8dd1a8ac11bbf921386d1f05da32bbf84640646093d1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnContactProps(
            alias=alias, display_name=display_name, type=type, plan=plan
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1230b668b68ef75e2be0ce9ce5bf14b7bd3b3b8b362785f62b8727c5094d5496)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3a35478651edceaa8211ec1ec74ee20552b26c38b90ed6598a8f22b7a3324e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the ``Contact`` resource, such as ``arn:aws:ssm-contacts:us-west-2:123456789012:contact/contactalias`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> builtins.str:
        '''The unique and identifiable alias of the contact or escalation plan.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-alias
        '''
        return typing.cast(builtins.str, jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e5a583902645e320f5f0d421b8847dd608990992c74ef2c375c9883591a4e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        '''The full name of the contact or escalation plan.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-displayname
        '''
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__634d931c33dc249f0a936122628bdb785fe509e48fda71d174f94247ec282c98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''Refers to the type of contact:.

        - ``PERSONAL`` : A single, individual contact.
        - ``ESCALATION`` : An escalation plan.
        - ``ONCALL_SCHEDULE`` : An on-call schedule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e692648e4215a1fe47c884b97b303f2d8f54f2325bc4e89fe8459ba378deceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="plan")
    def plan(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnContact.StageProperty", _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''A list of stages.

        A contact has an engagement plan with stages that contact specified contact channels. An escalation plan uses stages that contact specified contacts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-plan
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnContact.StageProperty", _aws_cdk_core_f4b25747.IResolvable]]]], jsii.get(self, "plan"))

    @plan.setter
    def plan(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnContact.StageProperty", _aws_cdk_core_f4b25747.IResolvable]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4a5edb5d31e9dd3b301d72fb5451ca492b93ef830ef679d169226bba5835196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "plan", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnContact.ChannelTargetInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "channel_id": "channelId",
            "retry_interval_in_minutes": "retryIntervalInMinutes",
        },
    )
    class ChannelTargetInfoProperty:
        def __init__(
            self,
            *,
            channel_id: builtins.str,
            retry_interval_in_minutes: jsii.Number,
        ) -> None:
            '''Information about the contact channel that Incident Manager uses to engage the contact.

            :param channel_id: The Amazon Resource Name (ARN) of the contact channel.
            :param retry_interval_in_minutes: The number of minutes to wait before retrying to send engagement if the engagement initially failed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-channeltargetinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                channel_target_info_property = ssmcontacts.CfnContact.ChannelTargetInfoProperty(
                    channel_id="channelId",
                    retry_interval_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d1337d37b740eb0596a247fac45b9a6781be3af024b4c695bd779bac6c2fe61c)
                check_type(argname="argument channel_id", value=channel_id, expected_type=type_hints["channel_id"])
                check_type(argname="argument retry_interval_in_minutes", value=retry_interval_in_minutes, expected_type=type_hints["retry_interval_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "channel_id": channel_id,
                "retry_interval_in_minutes": retry_interval_in_minutes,
            }

        @builtins.property
        def channel_id(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the contact channel.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-channeltargetinfo.html#cfn-ssmcontacts-contact-channeltargetinfo-channelid
            '''
            result = self._values.get("channel_id")
            assert result is not None, "Required property 'channel_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def retry_interval_in_minutes(self) -> jsii.Number:
            '''The number of minutes to wait before retrying to send engagement if the engagement initially failed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-channeltargetinfo.html#cfn-ssmcontacts-contact-channeltargetinfo-retryintervalinminutes
            '''
            result = self._values.get("retry_interval_in_minutes")
            assert result is not None, "Required property 'retry_interval_in_minutes' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChannelTargetInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnContact.ContactTargetInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"contact_id": "contactId", "is_essential": "isEssential"},
    )
    class ContactTargetInfoProperty:
        def __init__(
            self,
            *,
            contact_id: builtins.str,
            is_essential: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        ) -> None:
            '''The contact that Incident Manager is engaging during an incident.

            :param contact_id: The Amazon Resource Name (ARN) of the contact.
            :param is_essential: A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-contacttargetinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                contact_target_info_property = ssmcontacts.CfnContact.ContactTargetInfoProperty(
                    contact_id="contactId",
                    is_essential=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27bb2669b4d0ea3739dd8e91f180cb5a526768e1b96634822e01f2d4c19391fc)
                check_type(argname="argument contact_id", value=contact_id, expected_type=type_hints["contact_id"])
                check_type(argname="argument is_essential", value=is_essential, expected_type=type_hints["is_essential"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "contact_id": contact_id,
                "is_essential": is_essential,
            }

        @builtins.property
        def contact_id(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the contact.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-contacttargetinfo.html#cfn-ssmcontacts-contact-contacttargetinfo-contactid
            '''
            result = self._values.get("contact_id")
            assert result is not None, "Required property 'contact_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def is_essential(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-contacttargetinfo.html#cfn-ssmcontacts-contact-contacttargetinfo-isessential
            '''
            result = self._values.get("is_essential")
            assert result is not None, "Required property 'is_essential' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContactTargetInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnContact.StageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "duration_in_minutes": "durationInMinutes",
            "targets": "targets",
        },
    )
    class StageProperty:
        def __init__(
            self,
            *,
            duration_in_minutes: jsii.Number,
            targets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnContact.TargetsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``Stage`` property type specifies a set amount of time that an escalation plan or engagement plan engages the specified contacts or contact methods.

            :param duration_in_minutes: The time to wait until beginning the next stage. The duration can only be set to 0 if a target is specified.
            :param targets: The contacts or contact methods that the escalation plan or engagement plan is engaging.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-stage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                stage_property = ssmcontacts.CfnContact.StageProperty(
                    duration_in_minutes=123,
                
                    # the properties below are optional
                    targets=[ssmcontacts.CfnContact.TargetsProperty(
                        channel_target_info=ssmcontacts.CfnContact.ChannelTargetInfoProperty(
                            channel_id="channelId",
                            retry_interval_in_minutes=123
                        ),
                        contact_target_info=ssmcontacts.CfnContact.ContactTargetInfoProperty(
                            contact_id="contactId",
                            is_essential=False
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dcdcb9e705292433792b822f72adb7e277c0c72e3b60b4012c590d2ec0dc30bb)
                check_type(argname="argument duration_in_minutes", value=duration_in_minutes, expected_type=type_hints["duration_in_minutes"])
                check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "duration_in_minutes": duration_in_minutes,
            }
            if targets is not None:
                self._values["targets"] = targets

        @builtins.property
        def duration_in_minutes(self) -> jsii.Number:
            '''The time to wait until beginning the next stage.

            The duration can only be set to 0 if a target is specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-stage.html#cfn-ssmcontacts-contact-stage-durationinminutes
            '''
            result = self._values.get("duration_in_minutes")
            assert result is not None, "Required property 'duration_in_minutes' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnContact.TargetsProperty"]]]]:
            '''The contacts or contact methods that the escalation plan or engagement plan is engaging.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-stage.html#cfn-ssmcontacts-contact-stage-targets
            '''
            result = self._values.get("targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnContact.TargetsProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnContact.TargetsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "channel_target_info": "channelTargetInfo",
            "contact_target_info": "contactTargetInfo",
        },
    )
    class TargetsProperty:
        def __init__(
            self,
            *,
            channel_target_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnContact.ChannelTargetInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            contact_target_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnContact.ContactTargetInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The contact or contact channel that's being engaged.

            :param channel_target_info: Information about the contact channel that Incident Manager engages.
            :param contact_target_info: The contact that Incident Manager is engaging during an incident.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-targets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                targets_property = ssmcontacts.CfnContact.TargetsProperty(
                    channel_target_info=ssmcontacts.CfnContact.ChannelTargetInfoProperty(
                        channel_id="channelId",
                        retry_interval_in_minutes=123
                    ),
                    contact_target_info=ssmcontacts.CfnContact.ContactTargetInfoProperty(
                        contact_id="contactId",
                        is_essential=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11e07482c664cb3a3264fa1f4d90282c886057cd7f89e833f40db9e670e0d9e8)
                check_type(argname="argument channel_target_info", value=channel_target_info, expected_type=type_hints["channel_target_info"])
                check_type(argname="argument contact_target_info", value=contact_target_info, expected_type=type_hints["contact_target_info"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if channel_target_info is not None:
                self._values["channel_target_info"] = channel_target_info
            if contact_target_info is not None:
                self._values["contact_target_info"] = contact_target_info

        @builtins.property
        def channel_target_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnContact.ChannelTargetInfoProperty"]]:
            '''Information about the contact channel that Incident Manager engages.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-targets.html#cfn-ssmcontacts-contact-targets-channeltargetinfo
            '''
            result = self._values.get("channel_target_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnContact.ChannelTargetInfoProperty"]], result)

        @builtins.property
        def contact_target_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnContact.ContactTargetInfoProperty"]]:
            '''The contact that Incident Manager is engaging during an incident.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-targets.html#cfn-ssmcontacts-contact-targets-contacttargetinfo
            '''
            result = self._values.get("contact_target_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnContact.ContactTargetInfoProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnContactChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssmcontacts.CfnContactChannel",
):
    '''A CloudFormation ``AWS::SSMContacts::ContactChannel``.

    The ``AWS::SSMContacts::ContactChannel`` resource specifies a contact channel as the method that Incident Manager uses to engage your contact.

    :cloudformationResource: AWS::SSMContacts::ContactChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ssmcontacts as ssmcontacts
        
        cfn_contact_channel = ssmcontacts.CfnContactChannel(self, "MyCfnContactChannel",
            channel_address="channelAddress",
            channel_name="channelName",
            channel_type="channelType",
            contact_id="contactId",
        
            # the properties below are optional
            defer_activation=False
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        channel_address: builtins.str,
        channel_name: builtins.str,
        channel_type: builtins.str,
        contact_id: builtins.str,
        defer_activation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::SSMContacts::ContactChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param channel_address: The details that Incident Manager uses when trying to engage the contact channel.
        :param channel_name: The name of the contact channel.
        :param channel_type: The type of the contact channel. Incident Manager supports three contact methods:. - SMS - VOICE - EMAIL
        :param contact_id: The Amazon Resource Name (ARN) of the contact you are adding the contact channel to.
        :param defer_activation: If you want to activate the channel at a later time, you can choose to defer activation. Incident Manager can't engage your contact channel until it has been activated.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d584ba0b5aff43f1a9062084e38be6f778d720246269c38be2f7bef856655007)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnContactChannelProps(
            channel_address=channel_address,
            channel_name=channel_name,
            channel_type=channel_type,
            contact_id=contact_id,
            defer_activation=defer_activation,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e53085b1f93febe9f9fa294dc08e8ac5dbf1eecc0515dfab3d618f15e61d6d6a)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0239a9c28f5fd7b8f3a42f37bb2f970b102231ca1d94ce3c54a587c498e7d72e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the ``ContactChannel`` resource.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="channelAddress")
    def channel_address(self) -> builtins.str:
        '''The details that Incident Manager uses when trying to engage the contact channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-channeladdress
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelAddress"))

    @channel_address.setter
    def channel_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b669043cb87e273af0357e950e61da4c14c15610728d1560c4bcff3a8cff6d31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelAddress", value)

    @builtins.property
    @jsii.member(jsii_name="channelName")
    def channel_name(self) -> builtins.str:
        '''The name of the contact channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-channelname
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelName"))

    @channel_name.setter
    def channel_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d135ce0b08cf07ac49939b1eb041ef56facd3c38aed94f6d137f621b8dd8c5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelName", value)

    @builtins.property
    @jsii.member(jsii_name="channelType")
    def channel_type(self) -> builtins.str:
        '''The type of the contact channel. Incident Manager supports three contact methods:.

        - SMS
        - VOICE
        - EMAIL

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-channeltype
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelType"))

    @channel_type.setter
    def channel_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c7101bcf899d638eabab4a048401067920e2213afa7ea8c504273ec1512a81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelType", value)

    @builtins.property
    @jsii.member(jsii_name="contactId")
    def contact_id(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the contact you are adding the contact channel to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-contactid
        '''
        return typing.cast(builtins.str, jsii.get(self, "contactId"))

    @contact_id.setter
    def contact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b2eb9dd7b9c19d9ec61bf2a3b780b5e6e3c94ae1eaf258d88b66a150785f401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactId", value)

    @builtins.property
    @jsii.member(jsii_name="deferActivation")
    def defer_activation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''If you want to activate the channel at a later time, you can choose to defer activation.

        Incident Manager can't engage your contact channel until it has been activated.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-deferactivation
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "deferActivation"))

    @defer_activation.setter
    def defer_activation(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8950bb0b7e2de2e25c77de7d5dbf6bdbaa3a77e7d3db453d8be0f3fe5203e062)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deferActivation", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssmcontacts.CfnContactChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_address": "channelAddress",
        "channel_name": "channelName",
        "channel_type": "channelType",
        "contact_id": "contactId",
        "defer_activation": "deferActivation",
    },
)
class CfnContactChannelProps:
    def __init__(
        self,
        *,
        channel_address: builtins.str,
        channel_name: builtins.str,
        channel_type: builtins.str,
        contact_id: builtins.str,
        defer_activation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnContactChannel``.

        :param channel_address: The details that Incident Manager uses when trying to engage the contact channel.
        :param channel_name: The name of the contact channel.
        :param channel_type: The type of the contact channel. Incident Manager supports three contact methods:. - SMS - VOICE - EMAIL
        :param contact_id: The Amazon Resource Name (ARN) of the contact you are adding the contact channel to.
        :param defer_activation: If you want to activate the channel at a later time, you can choose to defer activation. Incident Manager can't engage your contact channel until it has been activated.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ssmcontacts as ssmcontacts
            
            cfn_contact_channel_props = ssmcontacts.CfnContactChannelProps(
                channel_address="channelAddress",
                channel_name="channelName",
                channel_type="channelType",
                contact_id="contactId",
            
                # the properties below are optional
                defer_activation=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb34361fd8f5369e85c8e58a72f8a65d8e00b9cdb5e0de7b51360435ba152dc1)
            check_type(argname="argument channel_address", value=channel_address, expected_type=type_hints["channel_address"])
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument channel_type", value=channel_type, expected_type=type_hints["channel_type"])
            check_type(argname="argument contact_id", value=contact_id, expected_type=type_hints["contact_id"])
            check_type(argname="argument defer_activation", value=defer_activation, expected_type=type_hints["defer_activation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel_address": channel_address,
            "channel_name": channel_name,
            "channel_type": channel_type,
            "contact_id": contact_id,
        }
        if defer_activation is not None:
            self._values["defer_activation"] = defer_activation

    @builtins.property
    def channel_address(self) -> builtins.str:
        '''The details that Incident Manager uses when trying to engage the contact channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-channeladdress
        '''
        result = self._values.get("channel_address")
        assert result is not None, "Required property 'channel_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def channel_name(self) -> builtins.str:
        '''The name of the contact channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-channelname
        '''
        result = self._values.get("channel_name")
        assert result is not None, "Required property 'channel_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def channel_type(self) -> builtins.str:
        '''The type of the contact channel. Incident Manager supports three contact methods:.

        - SMS
        - VOICE
        - EMAIL

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-channeltype
        '''
        result = self._values.get("channel_type")
        assert result is not None, "Required property 'channel_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def contact_id(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the contact you are adding the contact channel to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-contactid
        '''
        result = self._values.get("contact_id")
        assert result is not None, "Required property 'contact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def defer_activation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''If you want to activate the channel at a later time, you can choose to defer activation.

        Incident Manager can't engage your contact channel until it has been activated.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-deferactivation
        '''
        result = self._values.get("defer_activation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssmcontacts.CfnContactProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "display_name": "displayName",
        "type": "type",
        "plan": "plan",
    },
)
class CfnContactProps:
    def __init__(
        self,
        *,
        alias: builtins.str,
        display_name: builtins.str,
        type: builtins.str,
        plan: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnContact.StageProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnContact``.

        :param alias: The unique and identifiable alias of the contact or escalation plan.
        :param display_name: The full name of the contact or escalation plan.
        :param type: Refers to the type of contact:. - ``PERSONAL`` : A single, individual contact. - ``ESCALATION`` : An escalation plan. - ``ONCALL_SCHEDULE`` : An on-call schedule.
        :param plan: A list of stages. A contact has an engagement plan with stages that contact specified contact channels. An escalation plan uses stages that contact specified contacts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ssmcontacts as ssmcontacts
            
            cfn_contact_props = ssmcontacts.CfnContactProps(
                alias="alias",
                display_name="displayName",
                type="type",
            
                # the properties below are optional
                plan=[ssmcontacts.CfnContact.StageProperty(
                    duration_in_minutes=123,
            
                    # the properties below are optional
                    targets=[ssmcontacts.CfnContact.TargetsProperty(
                        channel_target_info=ssmcontacts.CfnContact.ChannelTargetInfoProperty(
                            channel_id="channelId",
                            retry_interval_in_minutes=123
                        ),
                        contact_target_info=ssmcontacts.CfnContact.ContactTargetInfoProperty(
                            contact_id="contactId",
                            is_essential=False
                        )
                    )]
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae3cef560502ef946eae9a24a973123fbbe837d048d060e9dc0b6f9e02dfa28e)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument plan", value=plan, expected_type=type_hints["plan"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alias": alias,
            "display_name": display_name,
            "type": type,
        }
        if plan is not None:
            self._values["plan"] = plan

    @builtins.property
    def alias(self) -> builtins.str:
        '''The unique and identifiable alias of the contact or escalation plan.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-alias
        '''
        result = self._values.get("alias")
        assert result is not None, "Required property 'alias' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The full name of the contact or escalation plan.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-displayname
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Refers to the type of contact:.

        - ``PERSONAL`` : A single, individual contact.
        - ``ESCALATION`` : An escalation plan.
        - ``ONCALL_SCHEDULE`` : An on-call schedule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def plan(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnContact.StageProperty, _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''A list of stages.

        A contact has an engagement plan with stages that contact specified contact channels. An escalation plan uses stages that contact specified contacts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-plan
        '''
        result = self._values.get("plan")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnContact.StageProperty, _aws_cdk_core_f4b25747.IResolvable]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnContact",
    "CfnContactChannel",
    "CfnContactChannelProps",
    "CfnContactProps",
]

publication.publish()

def _typecheckingstub__1a6ca3ad36cfd3d6487f8dd1a8ac11bbf921386d1f05da32bbf84640646093d1(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    alias: builtins.str,
    display_name: builtins.str,
    type: builtins.str,
    plan: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnContact.StageProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1230b668b68ef75e2be0ce9ce5bf14b7bd3b3b8b362785f62b8727c5094d5496(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3a35478651edceaa8211ec1ec74ee20552b26c38b90ed6598a8f22b7a3324e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e5a583902645e320f5f0d421b8847dd608990992c74ef2c375c9883591a4e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__634d931c33dc249f0a936122628bdb785fe509e48fda71d174f94247ec282c98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e692648e4215a1fe47c884b97b303f2d8f54f2325bc4e89fe8459ba378deceb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a5edb5d31e9dd3b301d72fb5451ca492b93ef830ef679d169226bba5835196(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnContact.StageProperty, _aws_cdk_core_f4b25747.IResolvable]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1337d37b740eb0596a247fac45b9a6781be3af024b4c695bd779bac6c2fe61c(
    *,
    channel_id: builtins.str,
    retry_interval_in_minutes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27bb2669b4d0ea3739dd8e91f180cb5a526768e1b96634822e01f2d4c19391fc(
    *,
    contact_id: builtins.str,
    is_essential: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcdcb9e705292433792b822f72adb7e277c0c72e3b60b4012c590d2ec0dc30bb(
    *,
    duration_in_minutes: jsii.Number,
    targets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnContact.TargetsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e07482c664cb3a3264fa1f4d90282c886057cd7f89e833f40db9e670e0d9e8(
    *,
    channel_target_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnContact.ChannelTargetInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    contact_target_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnContact.ContactTargetInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d584ba0b5aff43f1a9062084e38be6f778d720246269c38be2f7bef856655007(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    channel_address: builtins.str,
    channel_name: builtins.str,
    channel_type: builtins.str,
    contact_id: builtins.str,
    defer_activation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53085b1f93febe9f9fa294dc08e8ac5dbf1eecc0515dfab3d618f15e61d6d6a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0239a9c28f5fd7b8f3a42f37bb2f970b102231ca1d94ce3c54a587c498e7d72e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b669043cb87e273af0357e950e61da4c14c15610728d1560c4bcff3a8cff6d31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d135ce0b08cf07ac49939b1eb041ef56facd3c38aed94f6d137f621b8dd8c5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c7101bcf899d638eabab4a048401067920e2213afa7ea8c504273ec1512a81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b2eb9dd7b9c19d9ec61bf2a3b780b5e6e3c94ae1eaf258d88b66a150785f401(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8950bb0b7e2de2e25c77de7d5dbf6bdbaa3a77e7d3db453d8be0f3fe5203e062(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb34361fd8f5369e85c8e58a72f8a65d8e00b9cdb5e0de7b51360435ba152dc1(
    *,
    channel_address: builtins.str,
    channel_name: builtins.str,
    channel_type: builtins.str,
    contact_id: builtins.str,
    defer_activation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3cef560502ef946eae9a24a973123fbbe837d048d060e9dc0b6f9e02dfa28e(
    *,
    alias: builtins.str,
    display_name: builtins.str,
    type: builtins.str,
    plan: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnContact.StageProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
