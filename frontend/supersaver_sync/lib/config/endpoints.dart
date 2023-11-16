import 'package:dio/dio.dart';

class Endpoints {
  Endpoints._();

  // base url
  static const String baseUrl = 'https://apistage.digitap.work/tds';

  // receiveTimeout
  static const Duration receiveTimeout = Duration(seconds: 4);

  // connectTimeout
  static const Duration connectionTimeout = Duration(seconds: 4);

  static const String coupons = '/offerings/coupons?mobile=1';
  static const String creditCards = '/offerings/credit_cards?mobile=1';

  static const String linkedBanks = '/profile/linked-banks?mobile=9640764764';
  static const String bankIdentifier =
      '/profile/transactions?bank_identifier=HDFC-FIP&mobile=9640764764&page=1';
  static const String dashoardAssets = '/dashboard/assets?mobile=9640764764';
  static const String dashoardLiabilities =
      '/dashboard/liabilities?mobile=9640764764';
  static const String dashboardEMI = '/dashboard/emi?mobile=9640764764';
}
