import 'package:fancy_drawer/fancy_drawer.dart';
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

class _HomePageMainState extends State<HomePageMain>
    with TickerProviderStateMixin {
  late PageController controller;
  int selected = 0;
  var heart = false;
  bool is_drawer_open = false;

  late FancyDrawerController _controller;

  late AnimationController _animationController;
  late Animation<double> _animation;
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    controller = PageController(initialPage: widget.defaultPage);
    selected = widget.defaultPage;
    _controller = FancyDrawerController(
        vsync: this, duration: const Duration(milliseconds: 250))
      ..addListener(() {
        setState(() {}); // Must call setState
      });

    _animationController = AnimationController(
      vsync: this,
      duration: Duration(milliseconds: 500),
    );

    _animation = Tween<double>(
      begin: 0,
      end: 1,
    ).animate(_animationController);
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        key: _scaffoldKey,
        drawer: Drawer(
          child: ListView(
            padding: EdgeInsets.zero,
            children: [
              DrawerHeader(
                decoration: BoxDecoration(
                  color: Color(0xAA004165),
                ),
                child: Text(
                  'SuperSaver Sync',
                  style: TextStyle(
                      color: Colors.white, fontWeight: FontWeight.w500),
                ),
              ),
              buildDrawerItem(Icons.house_rounded, 'Home', () {
                controller.jumpToPage(0);
                setState(() {
                  selected = 0;
                });
              }),
              buildDrawerItem(Icons.history, 'History', () {
                // Add functionality for History
                controller.jumpToPage(1);
                setState(() {
                  selected = 1;
                });
              }),
              buildDrawerItem(Icons.analytics, 'Analytics', () {
                // Add functionality for Analytics
                controller.jumpToPage(2);
                setState(() {
                  selected = 2;
                });
              }),
              buildDrawerItem(Icons.person, 'My Portfolio', () {
                // Add functionality for Account Info
                controller.jumpToPage(3);
                setState(() {
                  selected = 3;
                });
              }),
            ],
          ),
        ),
        backgroundColor: Colors.white,
        body: SafeArea(
          child: Column(
            children: [
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    IconButton(
                        onPressed: () {
                          if (_scaffoldKey.currentState!.isDrawerOpen) {
                            _scaffoldKey.currentState!.closeDrawer();
                          } else {
                            _scaffoldKey.currentState!.openDrawer();
                          }
                        },
                        icon: Icon(Icons.menu),
                        iconSize: 60,
                        color: Color(0xAA004165)),
                    InkWell(
                      onTap: () {
                        controller.jumpToPage(3);
                        setState(() {
                          selected = 3;
                        });
                      },
                      child: CircleAvatar(
                        radius: 25.0, // Adjust the radius as needed
                        backgroundColor:
                            Color(0xAA004165), // Set background color
                        child: Icon(
                          size: 50,
                          Icons.account_circle,
                          color: Colors.white, // Set icon color
                        ),
                      ),
                    )
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
                  Icons.analytics,
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
      ),
    );
  }

  Widget buildDrawerItem(IconData icon, String label, Function onTap) {
    return ListTile(
      leading: Icon(icon),
      title: Text(label),
      onTap: () {
        onTap();
        Navigator.pop(context); // Close the drawer after selecting an item
      },
    );
  }
}
