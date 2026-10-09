import 'dart:math';

/// Calculates exponential retry backoff intervals with jitter
/// Flow specified in Section 9:
/// (30s, 1m, 2m, 5m, then 15m cap) with jitter
class BackoffCalculator {
  static const List<Duration> retryIntervals = [
    Duration(seconds: 30),
    Duration(minutes: 1),
    Duration(minutes: 2),
    Duration(minutes: 5),
    Duration(minutes: 15),
  ];

  static Duration getNextInterval(int attempt, {Random? random}) {
    final rand = random ?? Random();
    final clampedAttempt = attempt.clamp(0, retryIntervals.length - 1);
    final baseDuration = retryIntervals[clampedAttempt];

    // Add +/- 10% jitter to prevent thundering herd problem
    final jitterFactor = 0.9 + (rand.nextDouble() * 0.2); // 0.90 to 1.10
    final milliseconds = (baseDuration.inMilliseconds * jitterFactor).round();

    return Duration(milliseconds: milliseconds);
  }

  static DateTime getNextAttemptTimestamp(int attempt, {DateTime? now, Random? random}) {
    final current = now ?? DateTime.now().toUtc();
    return current.add(getNextInterval(attempt, random: random));
  }
}
