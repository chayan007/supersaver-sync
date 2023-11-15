import 'package:json_annotation/json_annotation.dart';

part 'linked_banks.g.dart';

@JsonSerializable()
class LinkedBanks {
  @JsonKey(name: "bank_name")
  String bankName;
  @JsonKey(name: "bank_account")
  String bankAccount;
  @JsonKey(name: "bank_identifier")
  String bankIdentifier;
  @JsonKey(name: "bank_logo")
  String bankLogo;

  LinkedBanks({
    required this.bankName,
    required this.bankAccount,
    required this.bankIdentifier,
    required this.bankLogo,
  });

  factory LinkedBanks.fromJson(Map<String, dynamic> json) =>
      _$LinkedBanksFromJson(json);

  Map<String, dynamic> toJson() => _$LinkedBanksToJson(this);
}
