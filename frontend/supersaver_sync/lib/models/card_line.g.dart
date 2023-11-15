// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'card_line.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

CardLine _$CardLineFromJson(Map<String, dynamic> json) => CardLine(
      creditCardName: json['credit_card_name'] as String,
      targetVendor: json['target_vendor'] as String,
      alternateVendors: (json['alternate_vendors'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      minimumCreditScore: json['minimum_credit_score'] as int,
      description: json['description'] as String,
    );

Map<String, dynamic> _$CardLineToJson(CardLine instance) => <String, dynamic>{
      'credit_card_name': instance.creditCardName,
      'target_vendor': instance.targetVendor,
      'alternate_vendors': instance.alternateVendors,
      'minimum_credit_score': instance.minimumCreditScore,
      'description': instance.description,
    };
