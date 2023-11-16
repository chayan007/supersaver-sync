import 'package:json_annotation/json_annotation.dart';

part 'card_line.g.dart';

@JsonSerializable()
class CardLine {
  @JsonKey(name: "credit_card_name")
  String creditCardName;
  @JsonKey(name: "target_vendor")
  String targetVendor;
  @JsonKey(name: "alternate_vendors")
  List<String> alternateVendors;
  @JsonKey(name: "minimum_credit_score")
  int minimumCreditScore;
  @JsonKey(name: "description")
  String description;

  CardLine({
    required this.creditCardName,
    required this.targetVendor,
    required this.alternateVendors,
    required this.minimumCreditScore,
    required this.description,
  });

  factory CardLine.fromJson(Map<String, dynamic> json) =>
      _$CardLineFromJson(json);

  Map<String, dynamic> toJson() => _$CardLineToJson(this);
}
