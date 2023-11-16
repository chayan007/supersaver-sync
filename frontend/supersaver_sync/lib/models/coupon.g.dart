// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'coupon.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Coupon _$CouponFromJson(Map<String, dynamic> json) => Coupon(
      couponName: json['coupon_name'] as String,
      couponCode: json['coupon_code'] as String,
      targetVendor: json['target_vendor'] as String,
      alternateVendors: (json['alternate_vendors'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      discountRate: json['discount_rate'] as int,
      discountAmount: json['discount_amount'] as int,
      discountLimit: json['discount_limit'] as int,
      description: json['description'] as String,
      couponHexCode: json['coupon_hex_code'] as String,
    );

Map<String, dynamic> _$CouponToJson(Coupon instance) => <String, dynamic>{
      'coupon_name': instance.couponName,
      'coupon_code': instance.couponCode,
      'target_vendor': instance.targetVendor,
      'alternate_vendors': instance.alternateVendors,
      'discount_rate': instance.discountRate,
      'discount_amount': instance.discountAmount,
      'discount_limit': instance.discountLimit,
      'description': instance.description,
      'coupon_hex_code': instance.couponHexCode,
    };
