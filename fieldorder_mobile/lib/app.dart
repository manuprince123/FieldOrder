import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'core/theme/app_theme.dart';
import 'features/orders/presentation/bloc/cart_bloc.dart';
import 'features/orders/presentation/bloc/sync_cubit.dart';
import 'features/dashboard/presentation/pages/dashboard_page.dart';

class FieldOrderApp extends StatefulWidget {
  const FieldOrderApp({super.key});

  @override
  State<FieldOrderApp> createState() => _FieldOrderAppState();
}

class _FieldOrderAppState extends State<FieldOrderApp> {
  int _currentTabIndex = 0;

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider<CartBloc>(create: (_) => CartBloc()),
        BlocProvider<SyncCubit>(create: (_) => SyncCubit()),
      ],
      child: MaterialApp(
        title: 'FieldOrder',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.lightTheme,
        darkTheme: AppTheme.darkTheme,
        themeMode: ThemeMode.light,
        home: Scaffold(
          body: IndexedStack(
            index: _currentTabIndex,
            children: [
              DashboardPage(
                onNewOrderTap: () => setState(() => _currentTabIndex = 1),
                onBrowseCatalogTap: () => setState(() => _currentTabIndex = 2),
                onSyncTap: () => setState(() => _currentTabIndex = 4),
                onAiOrderTap: () => _showAiOrderBottomSheet(context),
              ),
              const Center(child: Text('Customer Directory (Search <3s, City Filter)')),
              const Center(child: Text('500 Product Catalog & Multi-Unit Selector')),
              const Center(child: Text('Shopping Cart & Multi-Tier Pricing Engine')),
              const Center(child: Text('Offline Outbox Queue & Sync Manager')),
            ],
          ),
          bottomNavigationBar: NavigationBar(
            selectedIndex: _currentTabIndex,
            onDestinationSelected: (index) => setState(() => _currentTabIndex = index),
            destinations: const [
              NavigationDestination(icon: Icon(Icons.dashboard_outlined), label: 'Home'),
              NavigationDestination(icon: Icon(Icons.people_outline), label: 'Customers'),
              NavigationDestination(icon: Icon(Icons.inventory_2_outlined), label: 'Catalog'),
              NavigationDestination(icon: Icon(Icons.shopping_cart_outlined), label: 'Cart'),
              NavigationDestination(icon: Icon(Icons.sync_rounded), label: 'Sync'),
            ],
          ),
        ),
      ),
    );
  }

  void _showAiOrderBottomSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (ctx) => Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'AI Natural Language Order Entry',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 8),
            const Text(
              'Type or speak: "10 cartons Maggi and 5 boxes Parle-G for Raju Traders"',
              style: TextStyle(fontSize: 12, color: Colors.grey),
            ),
            const SizedBox(height: 14),
            TextField(
              maxLines: 3,
              decoration: InputDecoration(
                hintText: 'Enter wholesale order details...',
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => Navigator.pop(ctx),
              child: const Text('Parse into Structured Cart Lines'),
            ),
          ],
        ),
      ),
    );
  }
}
