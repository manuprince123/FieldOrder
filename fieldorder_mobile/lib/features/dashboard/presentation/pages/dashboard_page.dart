import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';

class DashboardPage extends StatelessWidget {
  final VoidCallback onNewOrderTap;
  final VoidCallback onBrowseCatalogTap;
  final VoidCallback onSyncTap;
  final VoidCallback onAiOrderTap;

  const DashboardPage({
    super.key,
    required this.onNewOrderTap,
    required this.onBrowseCatalogTap,
    required this.onSyncTap,
    required this.onAiOrderTap,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Vikram Rathore',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700),
            ),
            Text(
              'South Zone • Route #4 (Active)',
              style: TextStyle(fontSize: 11, color: AppColors.lightSubText),
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.sync_rounded),
            onPressed: onSyncTap,
            tooltip: 'Sync Status',
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Offline / Sync Status Card
          Card(
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Row(
                children: [
                  Container(
                    width: 10,
                    height: 10,
                    decoration: const BoxDecoration(
                      color: AppColors.statusSynced,
                      shape: BoxShape.circle,
                    ),
                  ),
                  const SizedBox(width: 10),
                  const Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Drift SQLite Engine Synced',
                          style: TextStyle(fontWeight: FontWeight.w700, fontSize: 13),
                        ),
                        Text(
                          '50 Customers • 500 Products cached',
                          style: TextStyle(fontSize: 11, color: AppColors.lightSubText),
                        ),
                      ],
                    ),
                  ),
                  TextButton(
                    onPressed: onSyncTap,
                    child: const Text('Outbox (0)'),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Daily KPIs
          Row(
            children: [
              Expanded(
                child: Card(
                  child: Padding(
                    padding: const EdgeInsets.all(14),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          "Today's Orders",
                          style: TextStyle(fontSize: 12, color: AppColors.lightSubText),
                        ),
                        const SizedBox(height: 4),
                        const Text(
                          '4',
                          style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          'All synced to ERP',
                          style: TextStyle(fontSize: 10, color: Colors.green.shade700, fontWeight: FontWeight.w600),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Card(
                  color: AppColors.brandNavy,
                  child: const Padding(
                    padding: EdgeInsets.all(14),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "Today's Bookings",
                          style: TextStyle(fontSize: 12, color: Colors.white70),
                        ),
                        SizedBox(height: 4),
                        Text(
                          '₹48,250',
                          style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: Colors.white),
                        ),
                        SizedBox(height: 2),
                        Text(
                          'Target: ₹60,000',
                          style: TextStyle(fontSize: 10, color: Colors.white60),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),

          // Action Grid
          ElevatedButton.icon(
            onPressed: onNewOrderTap,
            icon: const Icon(Icons.person_search_rounded),
            label: const Text('Start New Order (Pick Customer)'),
          ),
          const SizedBox(height: 10),
          OutlinedButton.icon(
            onPressed: onAiOrderTap,
            icon: const Icon(Icons.auto_awesome, color: Colors.purple),
            label: const Text('AI Voice / Free-Text Order Entry'),
            style: OutlinedButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
              side: const BorderSide(color: Colors.purple),
            ),
          ),
          const SizedBox(height: 10),
          OutlinedButton.icon(
            onPressed: onBrowseCatalogTap,
            icon: const Icon(Icons.inventory_2_outlined),
            label: const Text('Browse 500 Product Catalog'),
            style: OutlinedButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
            ),
          ),
        ],
      ),
    );
  }
}
