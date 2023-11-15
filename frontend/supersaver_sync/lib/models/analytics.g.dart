// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'analytics.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Analytics _$AnalyticsFromJson(Map<String, dynamic> json) => Analytics(
      category: json['category'] as String,
      sumOfAmount: (json['sum of amount'] as num).toDouble(),
      count: json['count'] as int,
    );

Map<String, dynamic> _$AnalyticsToJson(Analytics instance) => <String, dynamic>{
      'category': instance.category,
      'sum of amount': instance.sumOfAmount,
      'count': instance.count,
    };
