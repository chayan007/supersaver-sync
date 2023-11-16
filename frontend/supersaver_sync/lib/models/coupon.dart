import 'package:json_annotation/json_annotation.dart';

part 'coupon.g.dart';

@JsonSerializable()
class Coupon {
  @JsonKey(name: "coupon_name")
  String couponName;
  @JsonKey(name: "coupon_code")
  String couponCode;
  @JsonKey(name: "target_vendor")
  String targetVendor;
  @JsonKey(name: "alternate_vendors")
  List<String> alternateVendors;
  @JsonKey(name: "discount_rate")
  int discountRate;
  @JsonKey(name: "discount_amount")
  int discountAmount;
  @JsonKey(name: "discount_limit")
  int discountLimit;
  @JsonKey(name: "description")
  String description;
  @JsonKey(name: "coupon_hex_code")
  String couponHexCode;

  Coupon({
    required this.couponName,
    required this.couponCode,
    required this.targetVendor,
    required this.alternateVendors,
    required this.discountRate,
    required this.discountAmount,
    required this.discountLimit,
    required this.description,
    required this.couponHexCode,
  });

  factory Coupon.fromJson(Map<String, dynamic> json) => _$CouponFromJson(json);

  Map<String, dynamic> toJson() => _$CouponToJson(this);
}
