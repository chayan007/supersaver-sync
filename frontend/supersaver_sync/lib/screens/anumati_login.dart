import 'package:flutter/material.dart';
import 'package:supersaver_sync/screens/aa_success_page.dart';

class AnumatiLogin extends StatefulWidget {
  const AnumatiLogin({Key? key}) : super(key: key);

  @override
  State<AnumatiLogin> createState() => _AnumatiLoginState();
}

class _AnumatiLoginState extends State<AnumatiLogin> {
  late double width, height;

  @override
  Widget build(BuildContext context) {
    width = MediaQuery.of(context).size.width;
    height = MediaQuery.of(context).size.height;
    return SafeArea(
      child: Scaffold(
        body: InkWell(
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => AnumatiSync()),
          ),
          child: Image.asset(
              width: width, height: height, 'assets/image/anumati_login.png'),
        ),
      ),
    );
  }
}

class AnumatiSync extends StatefulWidget {
  const AnumatiSync({Key? key}) : super(key: key);

  @override
  State<AnumatiSync> createState() => _AnumatiSyncState();
}

class _AnumatiSyncState extends State<AnumatiSync> {
  late double width, height;

  @override
  Widget build(BuildContext context) {
    width = MediaQuery.of(context).size.width;
    height = MediaQuery.of(context).size.height;
    return SafeArea(
      child: Scaffold(
        body: InkWell(
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => AASuccessPage()),
          ),
          child: Image.asset(
              width: width, height: height, 'assets/image/anumati_sync.png'),
        ),
      ),
    );
  }
}
