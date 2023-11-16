import 'dart:convert';

import 'package:awesome_card/awesome_card.dart';
import 'package:http/http.dart' as http;

import 'package:coupon_uikit/coupon_uikit.dart';
import 'package:flutter/material.dart';
import 'package:supersaver_sync/config/endpoints.dart';
import 'package:supersaver_sync/models/card_line.dart';
import 'package:supersaver_sync/models/coupon.dart';

class CouponListPage extends StatefulWidget {
  const CouponListPage({super.key});

  @override
  State<CouponListPage> createState() => _CouponListPageState();
}

class _CouponListPageState extends State<CouponListPage> {
  var category = ['Current Vendor', 'Alternate Vendor', 'Credit Line Vendor'];
  int i = 0;
  int selected = 0;
  int tag = -1;
  late double width;
  late double height;
  String _apiUrl = Endpoints.baseUrl + Endpoints.coupons;
  List<Coupon> _responseData = [];
  List<CardLine> _cardResponseData = [];

  Map<int, Map<String, String>> mapChips = {
    0: {
      "title": "Coupons Waiting For You",
      "api_url": Endpoints.baseUrl + Endpoints.coupons,
      "image_url": "https://img.icons8.com/ios/50/budget.png"
    },
    1: {
      "title": "Coupons Waiting For You",
      "api_url": Endpoints.baseUrl + Endpoints.alternateCoupons,
      "image_url": "https://img.icons8.com/ios/50/budget.png"
    },
    2: {
      "title": "List of Credit Cards ",
      "api_url": Endpoints.baseUrl + Endpoints.creditCards
    }
  };

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _fetchData();
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

  Color stringToColor(String hexColor, {String type = 'secondary'}) {
    hexColor = hexColor.toUpperCase().replaceAll("#", "");

    if (hexColor.length == 6 && type == "primary") {
      hexColor = "33" + hexColor;
    }

    if (hexColor.length == 6 && type != "primary") {
      hexColor = "FF" + hexColor;
    }

    return Color(int.parse(hexColor, radix: 16));
  }

  Widget buildCouponItem(Coupon item) {
    // const Color primaryColor = Color(0xffcbf3f0);
    // const Color secondaryColor = Color(0xff368f8b);
    Color primaryColor = stringToColor(item.couponHexCode, type: 'primary');
    Color secondaryColor = stringToColor(item.couponHexCode);
    return CouponCard(
      height: 150,
      backgroundColor: primaryColor,
      curveAxis: Axis.vertical,
      firstChild: Container(
        decoration: BoxDecoration(
          color: secondaryColor,
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Expanded(
              child: Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      (item.discountAmount == 0)
                          ? item.discountRate!.toString() + "%"
                          : item.discountAmount!.toString() + "₹",
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    Text(
                      'OFF',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const Divider(color: Colors.white54, height: 0),
            Expanded(
              child: Center(
                child: Text(
                  item.couponName!,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
      secondChild: Container(
        width: double.maxFinite,
        padding: const EdgeInsets.all(18),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Coupon Code',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.bold,
                color: Colors.black54,
              ),
            ),
            SizedBox(height: 4),
            Text(
              item.couponCode!,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 24,
                color: secondaryColor,
                fontWeight: FontWeight.bold,
              ),
            ),
            Spacer(),
            Text(
              (item.discountLimit != 0)
                  ? "Upto: " + item.discountLimit!.toString() + " ₹"
                  : "",
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Colors.black45,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget buildCardItem(CardLine item) {
    return Padding(
        padding: const EdgeInsets.only(right: 0),
        child: Column(
          children: [
            CreditCard(
                cardNumber: "XXXX XXXX XXXX 7854",
                cardHolderName: "CHAYAN DATTA",
                cvv: "XXX",
                bankName: item.creditCardName,
                cardType: CardType
                    .masterCard, // Optional if you want to override Card Type
                showBackSide: false,
                frontBackground: CardBackgrounds.black,
                backBackground: CardBackgrounds.white,
                textName: 'Name',
                textExpiry: 'MM/YY'),
            SizedBox(
              height: 10,
            ),
            ElevatedButton(
              onPressed: () {},
              child: Text(
                'APPLY NOW',
                style: TextStyle(color: Colors.white),
              ),
              style: ElevatedButton.styleFrom(
                  padding: EdgeInsets.symmetric(horizontal: width * 0.3),
                  backgroundColor: Color(0xAA004165),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8.0))),
            ),
          ],
        ));
  }

  @override
  Widget build(BuildContext context) {
    width = MediaQuery.of(context).size.width;
    height = MediaQuery.of(context).size.height;

    return Container(
      padding: EdgeInsets.only(left: 20),
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(
              height: height * .02,
            ),
            SizedBox(
              height: height * .02,
            ),
            _buildChipList(context),
            SizedBox(
              height: height * .02,
            ),
            Text(
              mapChips[selected]!["title"]!,
              style: TextStyle(
                  fontWeight: FontWeight.w700,
                  color: Color(0xAA004165),
                  fontSize: 24),
            ),
            SizedBox(
              height: height * .02,
            ),
            Padding(
              padding: const EdgeInsets.only(right: 20),
              child: ((_responseData.length != 0 && selected != 2) ||
                      _cardResponseData.length != 0)
                  ? ListView.builder(
                      itemCount: (selected != 2)
                          ? _responseData.length
                          : _cardResponseData.length,
                      shrinkWrap: true,
                      physics: BouncingScrollPhysics(),
                      itemBuilder: (context, index) {
                        return Padding(
                          padding: EdgeInsets.symmetric(vertical: 10),
                          child: (selected != 2)
                              ? buildCouponItem(_responseData[index])
                              : buildCardItem(_cardResponseData[index]),
                        );
                      },
                    )
                  : CircularProgressIndicator(),
            )
          ],
        ),
      ),
    );
  }

  Future<void> _fetchData() async {
    try {
      print("URL:" + mapChips[selected]!["api_url"]!);
      http.Response response =
          await http.get(Uri.parse(mapChips[selected]!["api_url"]!));

      if (response.statusCode == 200) {
        List<dynamic> data = json.decode(response.body) as List<dynamic>;

        setState(() {
          if (selected == 2) {
            _cardResponseData = data
                .map((json) => CardLine.fromJson(json as Map<String, dynamic>))
                .toList();
            _responseData = [];
            print(_cardResponseData);
          } else {
            _responseData = data
                .map((json) => Coupon.fromJson(json as Map<String, dynamic>))
                .toList();
            _cardResponseData = [];
          }
        });
      } else {
        print('Failed to load data. Status code: ${response.statusCode}');
      }
    } catch (error) {
      print('Error: $error');
    }
  }
}
