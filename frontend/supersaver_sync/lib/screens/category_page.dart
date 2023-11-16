import 'dart:convert';

import 'package:cached_network_image/cached_network_image.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:supersaver_sync/config/endpoints.dart';
import 'package:supersaver_sync/models/analytics.dart';
import 'package:supersaver_sync/widgets/line_chart.dart';
import 'package:http/http.dart' as http;

class CategoryPage extends StatefulWidget {
  const CategoryPage({super.key});

  @override
  State<CategoryPage> createState() => _CategoryPageState();
}

class _CategoryPageState extends State<CategoryPage> {
  var category = ['Income', 'Expenditures', 'EMIs'];
  int i = 0;
  int selected = 0;
  int tag = -1;
  late double width;
  late double height;
  String _apiUrl = Endpoints.baseUrl + Endpoints.linkedBanks;
  List<Analytics> _responseData = [];

  Map<int, Map<String, String>> mapChips = {
    0: {
      "title": "Income Graph",
      "subtitle": "Income Categories",
      "api_url": Endpoints.baseUrl + Endpoints.dashoardAssets,
      "image_url": "https://img.icons8.com/ios/50/budget.png"
    },
    1: {
      "title": "Expenditure Graph",
      "subtitle": "Expenditure  Categories",
      "api_url": Endpoints.baseUrl + Endpoints.dashoardLiabilities,
      "image_url": "https://img.icons8.com/officel/80/piping.png"
    },
    2: {
      "title": "EMI Graph",
      "subtitle": "EMI  Categories",
      "api_url": Endpoints.baseUrl + Endpoints.dashboardEMI,
      "image_url": "https://img.icons8.com/parakeet/48/buy-now-pay-later.png"
    }
  };

  List<Map<String, String>> allCategoryData = [
    {
      "amount": "30,000",
      "img_url": "https://img.icons8.com/ios/50/budget.png",
      "type": "Salary",
      "percent_contribution": "100%"
    },
    {
      "amount": "40,000",
      "img_url": "https://img.icons8.com/ios/50/budget.png",
      "type": "Rental Income",
      "percent_contribution": "60%"
    },
    {
      "amount": "30,000",
      "img_url": "https://img.icons8.com/ios/50/budget.png",
      "type": "Trading",
      "percent_contribution": "20%"
    }
  ];

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _fetchData();
  }

  Widget buildNavItem(
    String msg,
    int value,
  ) {
    return Padding(
      padding: const EdgeInsets.only(right: 10),
      child: InkWell(
        onTap: () {
          _responseData = [];
          setState(() {
            selected = value;
          });
          _fetchData();
        },
        child: Container(
          padding: EdgeInsets.symmetric(horizontal: 10),
          alignment: Alignment.center,
          // width: 70,
          decoration: BoxDecoration(
              border: Border.all(color: Color(0xAA004165), width: 1.5),
              color:
                  (value == selected) ? Color(0xAA004165) : Colors.transparent,
              borderRadius: BorderRadius.circular(15)),
          child: Text(
            msg,
            style: TextStyle(
              color: (value == selected) ? Colors.white : Color(0xAA004165),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildChipList(BuildContext context) {
    return Container(
      width: width,
      height: 40,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: category.length,
        shrinkWrap: true,
        physics: BouncingScrollPhysics(),
        itemBuilder: (context, index) {
          return buildNavItem(category[index], index);
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    width = MediaQuery.of(context).size.width;
    height = MediaQuery.of(context).size.height;

    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 20),
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              mapChips[selected]!['title']!,
              style: TextStyle(
                  fontWeight: FontWeight.w700,
                  color: Color(0xAA004165),
                  fontSize: 24),
            ),
            SizedBox(
              height: 10,
            ),
            _buildChipList(context),
            SizedBox(
              height: 10,
            ),
            FlLineChart(chart_type: category[selected]),
            SizedBox(
              height: 10,
            ),
            Text(
              mapChips[selected]!['subtitle']!,
              style: TextStyle(
                  color: Color(0xAA004165),
                  fontWeight: FontWeight.bold,
                  fontSize: 20),
            ),
            SizedBox(
              height: 10,
            ),
            (_responseData.length != 0)
                ? SingleChildScrollView(
                    child: GridView.builder(
                        physics: NeverScrollableScrollPhysics(),
                        shrinkWrap: true,
                        itemCount: _responseData.length,
                        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                            crossAxisCount: 2,
                            crossAxisSpacing: 10,
                            mainAxisSpacing: 20),
                        itemBuilder: (context, index) {
                          return InkWell(
                            onTap: () {},
                            child: Card(
                              child: Padding(
                                padding: const EdgeInsets.all(8.0),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Container(
                                      width: width * 0.1,
                                      height: height * 0.07,
                                      child: CachedNetworkImage(
                                        imageUrl:
                                            mapChips[selected]!["image_url"]!,
                                        fit: BoxFit.contain,
                                        progressIndicatorBuilder:
                                            (context, url, downloadProgress) =>
                                                Container(
                                          width: 15,
                                          height: 15,
                                          child: CircularProgressIndicator(
                                              value: downloadProgress.progress),
                                        ),
                                        errorWidget: (context, url, error) =>
                                            Icon(Icons.error),
                                      ),
                                    ),
                                    Text(
                                      _responseData[index]
                                          .sumOfAmount
                                          .toString(),
                                      style: TextStyle(
                                          color: Color(0xAA363B64),
                                          fontWeight: FontWeight.bold,
                                          fontSize: 18),
                                    ),
                                    Text(
                                        _responseData[index].count!.toString()),
                                    SizedBox(
                                      height: 10,
                                    ),
                                    Text(
                                      _responseData[index].category,
                                      style:
                                          TextStyle(color: Color(0xFFADAFBD)),
                                    )
                                  ],
                                ),
                              ),
                            ),
                          );
                        }),
                  )
                : CircularProgressIndicator()
          ],
        ),
      ),
    );
  }

  Future<void> _fetchData() async {
    try {
      print("API triggered");
      http.Response response =
          await http.get(Uri.parse(mapChips[selected]!["api_url"]!));

      if (response.statusCode == 200) {
        List<dynamic> data = json.decode(response.body) as List<dynamic>;

        setState(() {
          _responseData = data
              .map((json) => Analytics.fromJson(json as Map<String, dynamic>))
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
