import 'package:flutter/material.dart';
import 'package:stylish_bottom_bar/model/bar_items.dart';
import 'package:stylish_bottom_bar/stylish_bottom_bar.dart';
import 'package:supersaver_sync/screens/account_page.dart';
import 'package:supersaver_sync/screens/category_page.dart';
import 'package:supersaver_sync/screens/coupon_list.dart';
import 'package:supersaver_sync/screens/history_page.dart';

class HomePageMain extends StatefulWidget {
  const HomePageMain({super.key, required this.defaultPage});
  final int defaultPage;

  @override
  State<HomePageMain> createState() => _HomePageMainState();
}

class _HomePageMainState extends State<HomePageMain> {
  late PageController controller;
  int selected = 0;
  var heart = false;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    controller = PageController(initialPage: widget.defaultPage);
    selected = widget.defaultPage;
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
        child: Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Row(
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
            ),
            Expanded(
              child: PageView(
                controller: controller,
                children: [
                  CouponListPage(),
                  HistoryPage(),
                  CategoryPage(),
                  AccountsPage()
                ],
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: StylishBottomBar(
        option: AnimatedBarOptions(
          barAnimation: BarAnimation.fade,
          iconStyle: IconStyle.animated,
        ),
        items: [
          BottomBarItem(
            icon: const Icon(
              Icons.house_outlined,
            ),
            selectedIcon: const Icon(Icons.house_rounded),
            selectedColor: Colors.teal,
            unSelectedColor: Colors.grey,
            title: const Text('Home'),
            badgeColor: Colors.purple,
          ),
          BottomBarItem(
            icon: const Icon(Icons.history_outlined),
            selectedIcon: const Icon(Icons.history_rounded),
            selectedColor: Colors.teal,
            unSelectedColor: Colors.grey,
            // backgroundColor: Colors.orange,
            title: const Text('History'),
          ),
          BottomBarItem(
              icon: const Icon(
                Icons.pie_chart_outline_outlined,
              ),
              selectedIcon: const Icon(
                Icons.pie_chart,
              ),
              selectedColor: Colors.teal,
              unSelectedColor: Colors.grey,
              title: const Text('Analytics')),
          BottomBarItem(
              icon: const Icon(
                Icons.person_outline,
              ),
              selectedIcon: const Icon(
                Icons.person,
              ),
              selectedColor: Colors.teal,
              unSelectedColor: Colors.grey,
              title: const Text('Profile')),
        ],
        currentIndex: selected,
        onTap: (index) {
          controller.jumpToPage(index);
          setState(() {
            selected = index;
          });
        },
      ),
    ));
  }
}
