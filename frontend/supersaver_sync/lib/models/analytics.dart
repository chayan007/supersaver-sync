import 'package:json_annotation/json_annotation.dart';

part 'analytics.g.dart';

@JsonSerializable()
class Analytics {
  @JsonKey(name: "category")
  String category;
  @JsonKey(name: "sum of amount")
  double sumOfAmount;
  @JsonKey(name: "count")
  int count;

  Analytics({
    required this.category,
    required this.sumOfAmount,
    required this.count,
  });

  factory Analytics.fromJson(Map<String, dynamic> json) =>
      _$AnalyticsFromJson(json);

  Map<String, dynamic> toJson() => _$AnalyticsToJson(this);
}
