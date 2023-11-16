import 'package:flutter/material.dart';

class HistoryPage extends StatefulWidget {
  HistoryPage({Key? key}) : super(key: key);

  @override
  State<HistoryPage> createState() => _HistoryPageState();
}

class _HistoryPageState extends State<HistoryPage> {
  List<Map<String, String>> historyData = [
    {
      "title": "Netflix",
      "subtitle": "14 Nov 2023",
      "image_url": "https://img.icons8.com/cute-clipart/64/netflix.png",
      "amount": "669.0"
    },
    {
      "title": "Amazon",
      "subtitle": "12 Nov 2023",
      "image_url": "https://img.icons8.com/office/30/amazon.png",
      "amount": "1200.0"
    },
    {
      "title": "Robert John",
      "subtitle": "05 NOV 2023",
      "image_url": "https://img.icons8.com/ios-filled/50/r.png",
      "amount": "830.04"
    },
    {
      "title": "David Ketod",
      "subtitle": "21 OCT 2023",
      "image_url": "https://img.icons8.com/color/48/d.png",
      "amount": "2541"
    },
    {
      "title": "Apple Music",
      "subtitle": "10 OCT 2023",
      "image_url": "https://img.icons8.com/color/48/apple-music.png",
      "amount": "99.0"
    },
    {
      "title": "KFC",
      "subtitle": "17 SEP 2023",
      "image_url": "https://img.icons8.com/color-glass/48/kfc-chicken.png",
      "amount": "1100"
    }
  ];
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: [
                Container(
                  padding: EdgeInsets.symmetric(horizontal: 20),
                  alignment: Alignment.center,
                  // width: 70,
                  decoration: BoxDecoration(
                      border: Border.all(color: Color(0xAA004165), width: 1.5),
                      color: Color(0xAA004165),
                      borderRadius: BorderRadius.circular(5)),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        "Total Savings",
                        style: TextStyle(color: Colors.white, fontSize: 16),
                      ),
                      SizedBox(
                        height: 5,
                      ),
                      Text(
                        "22,000 ",
                        style: TextStyle(
                          color: Color(0xFF64EDB2),
                        ),
                      ),
                      SizedBox(
                        height: 5,
                      ),
                      Text(
                        '02-Feb-2023 to today',
                        style: TextStyle(color: Colors.white, fontSize: 10),
                      )
                    ],
                  ),
                ),
                SizedBox(
                  width: 5,
                ),
                Container(
                  padding: EdgeInsets.symmetric(horizontal: 20),
                  alignment: Alignment.center,
                  // width: 70,
                  decoration: BoxDecoration(
                      border: Border.all(color: Color(0xAA004165), width: 1.5),
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(5)),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        "This Month",
                        style:
                            TextStyle(color: Color(0xAA004165), fontSize: 16),
                      ),
                      SizedBox(
                        height: 5,
                      ),
                      Text(
                        "5,000 ",
                        style: TextStyle(
                          color: Color(0xFF64EDB2),
                        ),
                      ),
                      SizedBox(
                        height: 5,
                      ),
                      Text(
                        '02-Feb-2023 to today',
                        style:
                            TextStyle(color: Color(0xAA004165), fontSize: 12),
                      )
                    ],
                  ),
                ),
                SizedBox(
                  width: 5,
                ),
                Container(
                  padding: EdgeInsets.symmetric(horizontal: 20),
                  alignment: Alignment.center,
                  // width: 70,
                  decoration: BoxDecoration(
                      border: Border.all(color: Color(0xAA004165), width: 1.5),
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(5)),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        "Unlocked Coupons",
                        style:
                            TextStyle(color: Color(0xAA004165), fontSize: 16),
                      ),
                      SizedBox(
                        height: 5,
                      ),
                      Text(
                        "5,000 ",
                        style: TextStyle(
                          color: Color(0xFF64EDB2),
                        ),
                      ),
                      SizedBox(
                        height: 5,
                      ),
                      Text(
                        '02-Feb-2023 to today',
                        style:
                            TextStyle(color: Color(0xAA004165), fontSize: 12),
                      )
                    ],
                  ),
                )
              ],
            ),
          ),
          SizedBox(
            height: 10,
          ),
          Text(
            "History",
            style: TextStyle(
                fontSize: 30,
                fontWeight: FontWeight.bold,
                color: Color(0xAA004165)),
          ),
          Expanded(
            child: ListView.builder(
              padding: EdgeInsets.only(right: 20),
              itemCount: historyData.length,
              shrinkWrap: true,
              physics: BouncingScrollPhysics(),
              itemBuilder: (context, index) {
                return Padding(
                  padding: EdgeInsets.symmetric(vertical: 3),
                  child: Card(
                    child: ListTile(
                      leading: Image.network(
                        historyData[index]!["image_url"]!,
                        height: 60,
                        width: 60,
                      ),
                      title: Text(
                        historyData[index]!["title"]!,
                        style: TextStyle(
                            fontWeight: FontWeight.w500, fontSize: 18),
                      ),
                      subtitle: Text(historyData[index]!["subtitle"]!),
                      trailing: Text(
                        historyData[index]!["amount"]!,
                        style: TextStyle(
                          color: Color(0xFF01D623),
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
        ],
      ),
    );
  }
}
