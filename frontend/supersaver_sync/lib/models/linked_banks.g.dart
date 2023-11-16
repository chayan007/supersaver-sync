// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'linked_banks.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

LinkedBanks _$LinkedBanksFromJson(Map<String, dynamic> json) => LinkedBanks(
      bankName: json['bank_name'] as String,
      bankAccount: json['bank_account'] as String,
      bankIdentifier: json['bank_identifier'] as String,
      bankLogo: json['bank_logo'] as String,
    );

Map<String, dynamic> _$LinkedBanksToJson(LinkedBanks instance) =>
    <String, dynamic>{
      'bank_name': instance.bankName,
      'bank_account': instance.bankAccount,
      'bank_identifier': instance.bankIdentifier,
      'bank_logo': instance.bankLogo,
    };
