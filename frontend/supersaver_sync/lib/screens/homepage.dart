import 'package:blur/blur.dart';
import 'package:coupon_uikit/coupon_uikit.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:supersaver_sync/screens/coupon_list.dart';
import 'package:supersaver_sync/screens/register_page.dart';

class HomePage extends StatefulWidget {
  HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  Widget buildCouponItem() {
    const Color primaryColor = Color(0xffcbf3f0);
    const Color secondaryColor = Color(0xff368f8b);
    return CouponCard(
      height: 150,
      backgroundColor: primaryColor,
      curveAxis: Axis.vertical,
      firstChild: Container(
        decoration: const BoxDecoration(
          color: secondaryColor,
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Expanded(
              child: Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: const [
                    Text(
                      '23%',
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
            const Expanded(
              child: Center(
                child: Text(
                  'WINTER IS\nHERE',
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
          children: const [
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
              'FREESALES',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 24,
                color: secondaryColor,
                fontWeight: FontWeight.bold,
              ),
            ),
            Spacer(),
            Text(
              'Valid Till - 30 Jan 2022',
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

  @override
  Widget build(BuildContext context) {
    SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle.light.copyWith(
      statusBarColor: Color(0xAA004165), // Change this to the desired color
      statusBarIconBrightness:
          Brightness.light, // Use dark icons on the status bar
    ));
    return SafeArea(
      child: Scaffold(
        body: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 30),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              SizedBox(
                height: 10,
              ),
              Card(
                child: Container(
                  child: Padding(
                    padding: const EdgeInsets.only(
                        bottom: 8, right: 8, left: 15, top: 8),
                    child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Welcome to AA future',
                            style: TextStyle(color: Color(0xAA004165)),
                          ),
                          SizedBox(
                            height: 5,
                          ),
                          Text(
                            'Check Coupons based on your Lifestyle',
                            style: TextStyle(
                                fontWeight: FontWeight.bold,
                                color: Color(0xAA004165)),
                          ),
                          SizedBox(
                            height: 10,
                          ),
                          ElevatedButton(
                            onPressed: () {
                              showDialog(
                                context: context,
                                builder: (BuildContext context) {
                                  return Dialog(
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(16.0),
                                    ),
                                    child: Column(
                                      mainAxisSize: MainAxisSize.min,
                                      children: [
                                        ClipRRect(
                                          borderRadius: BorderRadius.vertical(
                                              top: Radius.circular(16.0)),
                                          // child: Placeholder(),
                                          child: Image.asset(
                                            'assets/image/aa_dialog_img.png', // Replace with your image asset path
                                            height:
                                                300, // Adjust the height as needed
                                            width: double.infinity,
                                            fit: BoxFit.contain,
                                          ),
                                        ),
                                        // Padding(
                                        //   padding: EdgeInsets.all(16.0),
                                        //   child: Text(
                                        //     'Confirmation',
                                        //     style: TextStyle(
                                        //       fontWeight: FontWeight.bold,
                                        //       fontSize: 18.0,
                                        //     ),
                                        //   ),
                                        // ),
                                        // SizedBox(height: 8.0),
                                        Text(
                                          'Do you have an AA profile?',
                                          style: TextStyle(
                                              fontWeight: FontWeight.bold,
                                              fontSize: 20),
                                        ),
                                        SizedBox(height: 16.0),
                                        Column(
                                          mainAxisAlignment:
                                              MainAxisAlignment.spaceEvenly,
                                          children: [
                                            ElevatedButton(
                                              onPressed: () {
                                                // Handle "Yes" button press
                                                // Navigator.of(context)
                                                //     .pop(); // Close the dialog
                                                // Add your logic for "Yes" here
                                                Navigator.push(
                                                  context,
                                                  MaterialPageRoute(
                                                      builder: (context) =>
                                                          RegisterPage(
                                                            is_aa_profile: true,
                                                          )),
                                                );
                                              },
                                              child: Text(
                                                'YES',
                                                style: TextStyle(
                                                    color: Colors.white),
                                              ),
                                              style: ElevatedButton.styleFrom(
                                                  padding: EdgeInsets.symmetric(
                                                      horizontal: 100),
                                                  backgroundColor:
                                                      Color(0xAA004165),
                                                  shape: RoundedRectangleBorder(
                                                      borderRadius:
                                                          BorderRadius.circular(
                                                              8.0))),
                                            ),
                                            SizedBox(
                                              height: 5,
                                            ),
                                            ElevatedButton(
                                              onPressed: () {
                                                // Add your logic for "Yes" here
                                                Navigator.push(
                                                  context,
                                                  MaterialPageRoute(
                                                      builder: (context) =>
                                                          RegisterPage(
                                                            is_aa_profile:
                                                                false,
                                                          )),
                                                );
                                              },
                                              child: Text(
                                                'No',
                                                style: TextStyle(
                                                    color: Color(0xAA004165)),
                                              ),
                                              style: ElevatedButton.styleFrom(
                                                  padding: EdgeInsets.symmetric(
                                                      horizontal: 100),
                                                  shape: RoundedRectangleBorder(
                                                      borderRadius:
                                                          BorderRadius.circular(
                                                              8.0))),
                                            ),
                                          ],
                                        ),
                                        SizedBox(height: 16.0),
                                      ],
                                    ),
                                  );
                                },
                              );
                            },
                            child: Text(
                              'Get Coupons',
                              style: TextStyle(color: Color(0xAAFBFBFB)),
                            ),
                            style: ElevatedButton.styleFrom(
                                backgroundColor: Color(0xAA004165)),
                          )
                        ]),
                  ),
                ),
              ),
              SizedBox(
                height: 10,
              ),
              Text(
                'Trending Coupons',
                style: TextStyle(
                    color: Colors.white,
                    fontSize: 26,
                    fontWeight: FontWeight.w500),
              ),
              SizedBox(
                height: 10,
              ),
              Blur(blur: 3, child: buildCouponItem()),
              SizedBox(
                height: 20,
              ),
              Blur(blur: 3, child: buildCouponItem()),
              SizedBox(
                height: 20,
              ),
              Blur(blur: 3, child: buildCouponItem())
            ],
          ),
        ),
      ),
    );
  }
}
