import 'package:feature_discovery/feature_discovery.dart';
import 'package:flutter/material.dart';
import 'package:supersaver_sync/counter/counter.dart';
import 'package:supersaver_sync/l10n/l10n.dart';
import 'package:supersaver_sync/screens/homepage.dart';

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return FeatureDiscovery(
      child: MaterialApp(
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          appBarTheme: AppBarTheme(
            backgroundColor: Theme.of(context).colorScheme.inversePrimary,
          ),
          scaffoldBackgroundColor: Color(0xAA004165),
          useMaterial3: true,
        ),
        localizationsDelegates: AppLocalizations.localizationsDelegates,
        supportedLocales: AppLocalizations.supportedLocales,
        home: HomePage(),
      ),
    );
  }
}
