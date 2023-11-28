import 'package:clipboard/clipboard.dart';
import 'package:coupon_uikit/coupon_uikit.dart';
import 'package:flutter/material.dart';
import 'package:supersaver_sync/models/coupon.dart';
import 'package:toast/toast.dart';

class VerticalCoupon extends StatefulWidget {
  const VerticalCoupon(
      {Key? key, required this.couponItem, required this.primaryColor})
      : super(key: key);
  final Coupon couponItem;
  final Color primaryColor;

  @override
  State<VerticalCoupon> createState() => _VerticalCouponState();
}

class _VerticalCouponState extends State<VerticalCoupon> {
  @override
  Widget build(BuildContext context) {
    ToastContext().init(context);
    return SafeArea(
      child: Scaffold(
        appBar: AppBar(
            backgroundColor: Color.fromARGB(170, 1, 41, 62),
            leading: IconButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              icon: Icon(Icons.arrow_back_ios),
              color: Colors.grey,
            )),
        body: Center(
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: 15),
            child: CouponCard(
              height: 300,
              curvePosition: 180,
              curveRadius: 30,
              borderRadius: 10,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    widget.primaryColor.withAlpha(100),
                    widget.primaryColor,
                  ],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
              ),
              firstChild: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    widget.couponItem.couponName,
                    style: TextStyle(
                      color: Colors.white54,
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 10),
                  Text(
                    (widget.couponItem.discountAmount == 0)
                        ? widget.couponItem.discountRate.toString() + "%"
                        : widget.couponItem.discountAmount.toString() + "₹",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 56,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    'OFF',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 26,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        'CODE: ',
                        style: TextStyle(
                          color: Colors.white54,
                          fontSize: 26,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                      Text(
                        widget.couponItem.couponCode,
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 26,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  )
                ],
              ),
              secondChild: Container(
                width: double.maxFinite,
                decoration: const BoxDecoration(
                  border: Border(
                    top: BorderSide(color: Colors.white),
                  ),
                ),
                padding:
                    const EdgeInsets.symmetric(vertical: 24, horizontal: 42),
                child: ElevatedButton(
                  style: ButtonStyle(
                    shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                      RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(60),
                      ),
                    ),
                    padding: MaterialStateProperty.all<EdgeInsetsGeometry>(
                      const EdgeInsets.symmetric(horizontal: 80),
                    ),
                    backgroundColor: MaterialStateProperty.all<Color>(
                      Colors.white,
                    ),
                  ),
                  onPressed: () async {
                    // await ClickToCopy.copy(widget.couponItem.couponCode);
                    FlutterClipboard.copy(widget.couponItem.couponCode).then(
                        (value) => Toast.show("Coupon Copied",
                            duration: Toast.lengthShort,
                            gravity: Toast.bottom));
                  },
                  child: Text(
                    'COPY',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: widget.primaryColor.withAlpha(200),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
