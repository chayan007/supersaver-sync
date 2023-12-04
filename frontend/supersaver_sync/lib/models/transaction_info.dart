import 'package:json_annotation/json_annotation.dart';

part 'transaction_info.g.dart';

@JsonSerializable()
class TransactionInfo {
  @JsonKey(name: "amount")
  String amount;
  @JsonKey(name: "currentBalance")
  String currentBalance;
  @JsonKey(name: "mode")
  String mode;
  @JsonKey(name: "narration")
  String narration;
  @JsonKey(name: "reference")
  String reference;
  @JsonKey(name: "transactionTimestamp")
  DateTime transactionTimestamp;
  @JsonKey(name: "txnId")
  String txnId;
  @JsonKey(name: "type")
  String type;
  @JsonKey(name: "valueDate")
  DateTime valueDate;

  TransactionInfo(
      {required this.amount,
      required this.currentBalance,
      required this.mode,
      required this.narration,
      required this.reference,
      required this.transactionTimestamp,
      required this.txnId,
      required this.type,
      required this.valueDate});

  factory TransactionInfo.fromJson(Map<String, dynamic> json) =>
      _$TransactionInfoFromJson(json);

  Map<String, dynamic> toJson() => _$TransactionInfoToJson(this);
}
