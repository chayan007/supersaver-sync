import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:dio/dio.dart';
import 'package:supersaver_sync/config/endpoints.dart';
import 'package:supersaver_sync/models/linked_banks.dart';

class DioClient {
  DioClient(this._dio) {
    _dio
      ..options.baseUrl = Endpoints.baseUrl
      ..options.connectTimeout = 4000
      ..options.receiveTimeout = 4000
      ..options.responseType = ResponseType.json;
  }

  final Dio _dio;

  // Future<VehEmInfo> getVehicleInfo(
  //   String url,
  //   Map<String, dynamic> data,
  // ) async {
  //   // TODO: implement getVehicleInfo
  //   debugPrint('baseurl: ' + _dio.options.baseUrl);
  //   debugPrint('data' + data.toString());

  //   try {
  //     final response = await _dio.post<Map<String, dynamic>>(
  //       url,
  //       data: data,
  //     );

  //     debugPrint(response.data.toString());
  //     final vehInfo = VehEmInfo.fromJson(response.data!);

  //     return vehInfo;
  //   } catch (e) {
  //     debugPrint(e.toString());
  //     rethrow;
  //   }
  // }

  // @override
  // Future<bool> removeVehicleInfo(String url, Map<String, dynamic> data) async {
  //   // TODO: implement removeVehicleInfo
  //   debugPrint('baseurl: ' + _dio.options.baseUrl);
  //   debugPrint('data' + data.toString());

  //   try {
  //     final response = await _dio.post<String>(
  //       url,
  //       data: data,
  //     );

  //     debugPrint(response.data.toString());
  //     if (response.statusCode == 200) {
  //       return true;
  //     } else {
  //       return false;
  //     }
  //   } catch (e) {
  //     debugPrint(e.toString());
  //     throw Error();
  //   }
  // }

  // @override
  // Future<VehEmInfoCertificate> getCertificateInfo(
  //   String url,
  //   Map<String, dynamic> data,
  // ) async {
  //   debugPrint('baseurl: ' + _dio.options.baseUrl);
  //   debugPrint('data cert ' + data.toString());

  //   try {
  //     final response = await _dio.post<Map<String, dynamic>>(
  //       url,
  //       data: data,
  //     );

  //     // debugPrint("cert response" + response.data.toString());
  //     final vehInfo = VehEmInfoCertificate.fromJson(response.data!);

  //     return vehInfo;
  //   } catch (e) {
  //     debugPrint(e.toString());
  //     rethrow;
  //   }
  // }

  Future<LinkedBanks> getLinkedBanks(String url) async {
    final response = await _dio.get<Map<String, String>>(url);
    var responseData = response.data!;

    return LinkedBanks.fromJson(responseData);
  }
}
