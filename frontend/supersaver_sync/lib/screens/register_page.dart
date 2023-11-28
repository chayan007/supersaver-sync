import 'package:dropdown_textfield/dropdown_textfield.dart';
import 'package:flutter/material.dart';
import 'package:supersaver_sync/screens/aa_success_page.dart';
import 'package:supersaver_sync/screens/anumati_login.dart';
import 'package:supersaver_sync/screens/main_home.dart';

class RegisterPage extends StatefulWidget {
  RegisterPage({Key? key, required this.is_aa_profile}) : super(key: key);
  final bool is_aa_profile;

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        backgroundColor: Colors.white,
        bottomNavigationBar: Padding(
          padding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
          child: Text(
            'Disclaimer: AA records will be pulled daily for better recommendations',
            style: TextStyle(color: Colors.grey, fontWeight: FontWeight.w600),
          ),
        ),
        body: Padding(
          padding: EdgeInsets.symmetric(horizontal: 20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Register',
                style: TextStyle(
                  color: Color(0xAA004165),
                  fontSize: 40,
                  fontWeight: FontWeight.w600,
                ),
              ),
              SizedBox(
                height: 10,
              ),
              Text(
                'Please fill the below',
                style: TextStyle(color: Color(0xAA5A5A5A)),
              ),
              SizedBox(
                height: 20,
              ),
              TextField(
                decoration: InputDecoration(
                  hintText: 'Enter your Mobile number',
                  floatingLabelBehavior: FloatingLabelBehavior.always,
                  labelText: 'Mobile Number *',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.all(Radius.circular(12)),
                    borderSide: BorderSide(color: Color(0xAA004165)),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderSide: BorderSide(color: Color(0xAA004165), width: 2),
                  ),
                ),
              ),
              SizedBox(
                height: 30,
              ),
              if (widget.is_aa_profile)
                DropDownTextField(
                  // initialValue: "name4",
                  listSpace: 20,
                  listPadding: ListPadding(top: 20),
                  enableSearch: false,
                  textFieldDecoration: InputDecoration(hintText: 'Select AA*'),
                  validator: (value) {
                    if (value == null) {
                      return "Required field";
                    } else {
                      return null;
                    }
                  },
                  dropDownList: const [
                    DropDownValueModel(name: 'Sahamati', value: "value1"),
                    DropDownValueModel(name: 'Finvu', value: "value2"),
                    DropDownValueModel(name: 'oneMoney', value: "value3"),
                  ],
                  listTextStyle: const TextStyle(color: Color(0xAA004165)),
                  dropDownItemCount: 3,

                  onChanged: (val) {},
                ),
              SizedBox(
                height: 30,
              ),
              if (widget.is_aa_profile)
                DropDownTextField(
                  // initialValue: "name4",
                  listSpace: 20,
                  listPadding: ListPadding(top: 20),
                  enableSearch: false,
                  textFieldDecoration:
                      InputDecoration(hintText: 'select consent tenure'),
                  validator: (value) {
                    if (value == null) {
                      return "Required field";
                    } else {
                      return null;
                    }
                  },
                  dropDownList: const [
                    DropDownValueModel(value: '1', name: "1 months"),
                    DropDownValueModel(value: '2', name: "3 months"),
                    DropDownValueModel(value: '3', name: "6 months"),
                    DropDownValueModel(value: '3', name: "9 months"),
                    DropDownValueModel(value: '3', name: "12 months"),
                  ],
                  listTextStyle: const TextStyle(color: Color(0xAA004165)),
                  dropDownItemCount: 3,

                  onChanged: (val) {},
                ),
              SizedBox(
                height: 25,
              ),
              Center(
                child: ElevatedButton(
                  onPressed: () {
                    // Handle "Yes" button press
                    // Navigator.of(context)
                    //     .pop(); // Close the dialog
                    // Add your logic for "Yes" here
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => AnumatiLogin()),
                    );
                    // Navigator.push(
                    //   context,
                    //   MaterialPageRoute(builder: (context) => AASuccessPage()),
                    // );
                  },
                  child: Text(
                    'YES',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 20,
                        fontWeight: FontWeight.w600),
                  ),
                  style: ElevatedButton.styleFrom(
                      padding: EdgeInsets.symmetric(horizontal: 150),
                      backgroundColor: Color(0xAA004165),
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8.0))),
                ),
              ),
              SizedBox(
                height: 15,
              ),
              Center(
                child: Text(
                  'We are redirecting you to your AA Support',
                  style: TextStyle(color: Color(0xAA5A5A5A)),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}
