import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:supersaver_sync/app/app.dart';
import 'package:supersaver_sync/config/endpoints.dart';
import 'package:supersaver_sync/models/linked_banks.dart';
import 'package:supersaver_sync/screens/register_page.dart';
import 'package:supersaver_sync/screens/view_transaction.dart';
import 'package:supersaver_sync/services/dio_service.dart';

class AccountInfo extends StatefulWidget {
  AccountInfo({Key? key, required this.bank}) : super(key: key);
  final LinkedBanks bank;

  @override
  State<AccountInfo> createState() => _AccountInfoState();
}

class _AccountInfoState extends State<AccountInfo> {
  // Dio _dio = Dio();
  String _apiUrl = Endpoints.baseUrl + Endpoints.linkedBanks;
  List<LinkedBanks> _responseData = [];

  // @override
  // void initState() {
  //   // TODO: implement initState
  //   super.initState();
  //   _fetchData();
  // }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        backgroundColor: Colors.white,
        appBar: AppBar(
            leading: IconButton(
          onPressed: () {
            Navigator.of(context).pop();
          },
          icon: Icon(Icons.arrow_back_ios),
          color: Colors.grey,
        )),
        body: Container(
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: 20),
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              // Row(
              //   mainAxisAlignment: MainAxisAlignment.spaceBetween,
              //   children: [
              //     CircleAvatar(
              //       radius: 25.0, // Adjust the radius as needed
              //       backgroundColor: Color(0xAA004165), // Set background color
              //       child: Icon(
              //         size: 50,
              //         Icons.account_circle,
              //         color: Colors.white, // Set icon color
              //       ),
              //     ),
              //     IconButton(
              //         onPressed: () {},
              //         icon: Icon(
              //           Icons.menu,
              //           size: 60,
              //           color: Color(0xAA004165),
              //         ))
              //   ],
              // ),
              // IconButton(
              //     onPressed: () {
              //       Navigator.of(context).pop();
              //     },
              //     icon: Icon(
              //       Icons.arrow_back_ios_new,
              //       size: 25,
              //     )),
              Text(
                "Accounts Details",
                style: TextStyle(
                    fontSize: 30,
                    fontWeight: FontWeight.bold,
                    color: Color(0xAA004165)),
              ),
              Card(
                color: Color.fromARGB(170, 235, 238, 240),
                child: Column(
                  children: [
                    ListTile(
                        leading: Image.network(
                          widget.bank.bankLogo,
                          height: 60,
                          width: 60,
                        ),
                        title: Text(
                          widget.bank.bankName,
                          style: TextStyle(
                              fontWeight: FontWeight.w500, fontSize: 20),
                        ),
                        subtitle: Text(widget.bank.bankIdentifier),
                        trailing: Card(
                          child: Padding(
                            padding: const EdgeInsets.all(3.0),
                            child: Column(children: [
                              Text("A/C type"),
                              Text(
                                "Single",
                                style: TextStyle(fontWeight: FontWeight.w500),
                              )
                            ]),
                          ),
                        )),
                    SizedBox(
                      height: 10,
                    ),
                    Padding(
                      padding: EdgeInsets.symmetric(horizontal: 25),
                      child: Column(
                        children: [
                          Row(
                            children: [
                              Text("Name: "),
                              SizedBox(
                                width: 25,
                              ),
                              Text('Deepak')
                            ],
                          ),
                          Row(
                            children: [
                              Text("DOB: "),
                              SizedBox(
                                width: 35,
                              ),
                              Text('20-08-1997')
                            ],
                          ),
                          Row(
                            children: [
                              Text("Mobile: "),
                              SizedBox(
                                width: 20,
                              ),
                              Text('9189523254')
                            ],
                          ),
                          Row(
                            children: [
                              Text("Email: "),
                              SizedBox(
                                width: 30,
                              ),
                              Text('sehrawatdeep7121@gmail.com')
                            ],
                          ),
                          Row(
                            children: [
                              Text("Nominee: "),
                              SizedBox(
                                width: 10,
                              ),
                              Text('Registered')
                            ],
                          ),
                          Row(
                            children: [
                              Text("Pan Card: "),
                              SizedBox(
                                width: 9,
                              ),
                              Text('ELKPD0572H')
                            ],
                          ),
                          Row(
                            children: [
                              Text("Address: "),
                              SizedBox(
                                width: 10,
                              ),
                              Container(
                                width: 220,
                                child: Text(
                                    'SO SATYAWAN MALHAR SAFIDON JIND, MALAR HARYAN, A INDIA,WATER SUPPLY,KARNAL, HARYANA, INDIA,132039 '),
                              )
                            ],
                          )
                        ],
                      ),
                    )
                  ],
                ),
              ),
              SizedBox(
                height: 20,
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
                        'VIEW TRANSACTIONS',
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
              .map((json) => LinkedBanks.fromJson(json as Map<String, dynamic>))
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
