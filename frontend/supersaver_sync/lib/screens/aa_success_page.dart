import 'package:flutter/material.dart';
import 'package:supersaver_sync/screens/main_home.dart';

class AASuccessPage extends StatefulWidget {
  const AASuccessPage({super.key});

  @override
  State<AASuccessPage> createState() => _AASuccessPageState();
}

class _AASuccessPageState extends State<AASuccessPage> {
  @override
  Widget build(BuildContext context) {
    return SafeArea(
        child: Scaffold(
      backgroundColor: Colors.white,
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
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
            Column(
              children: [
                Text(
                  'Account Aggregator details fetched successfully',
                  style: TextStyle(
                      fontSize: 25,
                      color: Color(0xAA004165),
                      fontWeight: FontWeight.w600),
                ),
                SizedBox(
                  height: 20,
                ),
                ClipRRect(
                  borderRadius:
                      BorderRadius.vertical(top: Radius.circular(16.0)),
                  // child: Placeholder(),
                  child: Image.asset(
                    'assets/image/aa_complete.png', // Replace with your image asset path
                    height: 300, // Adjust the height as needed
                    width: double.infinity,
                    fit: BoxFit.contain,
                  ),
                )
              ],
            ),
            Center(
              child: ElevatedButton(
                onPressed: () {
                  Navigator.of(context).pop();
                  Navigator.of(context).pop();
                  Navigator.of(context).pop();
                  Navigator.of(context).pop();
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => HomePageMain()),
                  );
                },
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      'Continue',
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
            SizedBox()
          ],
        ),
      ),
    ));
  }
}
