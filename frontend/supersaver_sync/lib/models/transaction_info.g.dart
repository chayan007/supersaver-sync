// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'transaction_info.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

TransactionInfo _$TransactionInfoFromJson(Map<String, dynamic> json) =>
    TransactionInfo(
      amount: json['amount'] as String,
      currentBalance: json['currentBalance'] as String,
      mode: json['mode'] as String,
      narration: json['narration'] as String,
      reference: json['reference'] as String,
      transactionTimestamp:
          DateTime.parse(json['transactionTimestamp'] as String),
      txnId: json['txnId'] as String,
      type: json['type'] as String,
      valueDate: DateTime.parse(json['valueDate'] as String),
    );

Map<String, dynamic> _$TransactionInfoToJson(TransactionInfo instance) =>
    <String, dynamic>{
      'amount': instance.amount,
      'currentBalance': instance.currentBalance,
      'mode': instance.mode,
      'narration': instance.narration,
      'reference': instance.reference,
      'transactionTimestamp': instance.transactionTimestamp.toIso8601String(),
      'txnId': instance.txnId,
      'type': instance.type,
      'valueDate': instance.valueDate.toIso8601String(),
    };
