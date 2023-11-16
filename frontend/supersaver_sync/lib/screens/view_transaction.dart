import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';
import 'package:supersaver_sync/config/constants.dart';
import 'package:supersaver_sync/config/endpoints.dart';
import 'package:supersaver_sync/models/linked_banks.dart';
import 'package:supersaver_sync/models/transaction_info.dart';
import 'package:supersaver_sync/screens/register_page.dart';
import 'package:supersaver_sync/services/dio_service.dart';

class ViewTransaction extends StatefulWidget {
  ViewTransaction({Key? key}) : super(key: key);

  @override
  State<ViewTransaction> createState() => _ViewTransactionState();
}

class _ViewTransactionState extends State<ViewTransaction> {
  // Dio _dio = Dio();
  String _apiUrl = Endpoints.baseUrl + Endpoints.bankIdentifier;
  List<TransactionInfo> _responseData = [];
  final format = DateFormat('yyyy-MM-dd HH:mm');

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _fetchData();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        backgroundColor: Colors.white,
        body: Container(
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: 20),
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  CircleAvatar(
                    radius: 25.0, // Adjust the radius as needed
                    backgroundColor: Color(0xAA004165), // Set background color
                    child: Icon(
                      size: 50,
                      Icons.account_circle,
                      color: Colors.white, // Set icon color
                    ),
                  ),
                  IconButton(
                      onPressed: () {},
                      icon: Icon(
                        Icons.menu,
                        size: 60,
                        color: Color(0xAA004165),
                      ))
                ],
              ),
              Text(
                "Transaction",
                style: TextStyle(
                    fontSize: 30,
                    fontWeight: FontWeight.bold,
                    color: Color(0xAA004165)),
              ),
              _responseData.length != 0
                  ? Expanded(
                      child: ListView.builder(
                        itemCount: _responseData.length,
                        shrinkWrap: true,
                        physics: BouncingScrollPhysics(),
                        itemBuilder: (context, index) {
                          return Padding(
                            padding: EdgeInsets.symmetric(vertical: 3),
                            child: Card(
                              child: ListTile(
                                leading: Image.network(
                                  _responseData[index].type == "DEBIT"
                                      ? Constants.DEBIT_IMAGE_URL
                                      : Constants.CREDIT_IMAGE_URL,
                                  height: 60,
                                  width: 60,
                                ),
                                title: Text(
                                  (_responseData[index].narration.length > 15)
                                      ? _responseData[index]
                                              .narration
                                              .substring(0, 15) +
                                          "..."
                                      : _responseData[index].narration,
                                  style: TextStyle(
                                      fontWeight: FontWeight.w500,
                                      fontSize: 18),
                                ),
                                subtitle: Text(format.format(
                                    _responseData[index].transactionTimestamp)),
                                trailing: Text(
                                  _responseData[index].amount,
                                  style: TextStyle(
                                    color: _responseData[index].type == "DEBIT"
                                        ? Color(0xFFD68101)
                                        : Color(0xFF01D623),
                                    fontWeight: FontWeight.w700,
                                    fontSize: 14,
                                  ),
                                ),
                              ),
                            ),
                          );
                        },
                      ),
                    )
                  : CircularProgressIndicator(),
              SizedBox(
                height: 5,
              ),
              Center(
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => ViewTransaction()),
                    );
                  },
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        'DOWNLOAD AS PDF',
                        style: TextStyle(
                            color: Colors.white,
                            fontSize: 25,
                            fontWeight: FontWeight.w600),
                      ),
                    ],
                  ),
                  style: ElevatedButton.styleFrom(
                      backgroundColor: Color(0xAA004165),
                      padding: EdgeInsets.symmetric(horizontal: 50),
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8.0))),
                ),
              ),
              SizedBox(
                height: 10,
              )
            ]),
          ),
        ),
      ),
    );
  }

  // Future<void> _fetchData() async {
  //   try {
  //     print(_apiUrl);
  //     Response<Map<String, dynamic>> response = await _dio
  //         .get("https://mocki.io/v1/455bab38-c111-4492-9b4c-3fe09f55cc83");
  //     setState(() {
  //       var banks = LinkedBanks.fromJson(response.data!);
  //     });
  //   } catch (error) {
  //     print('Error fetching data: $error');
  //   }
  // }

  Future<void> _fetchData() async {
    try {
      http.Response response = await http.get(Uri.parse(_apiUrl));

      if (response.statusCode == 200) {
        List<dynamic> data = json.decode(response.body) as List<dynamic>;

        setState(() {
          _responseData = data
              .map((json) =>
                  TransactionInfo.fromJson(json as Map<String, dynamic>))
              .toList();
        });
      } else {
        print('Failed to load data. Status code: ${response.statusCode}');
      }
    } catch (error) {
      print('Error: $error');
    }
  }
}
