import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:supersaver_sync/config/endpoints.dart';
import 'package:supersaver_sync/models/linked_banks.dart';
import 'package:supersaver_sync/screens/account_info.dart';
import 'package:supersaver_sync/screens/register_page.dart';
import 'package:supersaver_sync/services/dio_service.dart';

class AccountsPage extends StatefulWidget {
  AccountsPage({Key? key}) : super(key: key);

  @override
  State<AccountsPage> createState() => _AccountsPageState();
}

class _AccountsPageState extends State<AccountsPage> {
  // Dio _dio = Dio();
  String _apiUrl = Endpoints.baseUrl + Endpoints.linkedBanks;
  List<LinkedBanks> _responseData = [];

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _fetchData();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 20),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(
          "Accounts",
          style: TextStyle(
              fontSize: 30,
              fontWeight: FontWeight.bold,
              color: Color(0xAA004165)),
        ),
        Card(
          color: Color.fromARGB(170, 235, 238, 240),
          child: Column(
            children: [
              _responseData.length != 0
                  ? ListView.builder(
                      itemCount: _responseData.length,
                      shrinkWrap: true,
                      physics: BouncingScrollPhysics(),
                      itemBuilder: (context, index) {
                        return ListTile(
                          leading: Image.network(
                            _responseData[index].bankLogo,
                            height: 60,
                            width: 60,
                          ),
                          title: Text(
                            _responseData[index].bankName!,
                            style: TextStyle(
                                fontWeight: FontWeight.w500, fontSize: 20),
                          ),
                          subtitle: Text(_responseData[index].bankIdentifier!),
                          trailing: ElevatedButton(
                            onPressed: () => Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) =>
                                      AccountInfo(bank: _responseData[index])),
                            ),
                            child: Text(
                              'View',
                              style: TextStyle(color: Colors.white),
                            ),
                            style: ElevatedButton.styleFrom(
                                shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(10)),
                                backgroundColor: Colors.blue),
                          ),
                        );
                      },
                    )
                  : CircularProgressIndicator(),
            ],
          ),
        ),
        SizedBox(
          height: 20,
        ),
        Center(
          child: ElevatedButton(
            onPressed: () {},
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  Icons.add_box_rounded,
                  color: Colors.white,
                  size: 30,
                ),
                SizedBox(
                  width: 10,
                ),
                Text(
                  'ADD ACCOUNT',
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
