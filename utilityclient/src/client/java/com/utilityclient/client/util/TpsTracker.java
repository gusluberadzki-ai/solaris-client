package com.utilityclient.client.util;

import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;

public final class TpsTracker {
    private static final int SAMPLE_SIZE = 20;
    private static final long[] tickIntervals = new long[SAMPLE_SIZE];
    private static int writeIndex = 0;
    private static int filled = 0;
    private static long lastTickTime = 0;
    private static double smoothedTps = 20.0;

    private TpsTracker() {}

    public static void register() {
        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            if (client.player == null) return;
            long now = System.currentTimeMillis();
            if (lastTickTime > 0) {
                long delta = now - lastTickTime;
                if (delta > 0 && delta < 5000) {
                    tickIntervals[writeIndex % SAMPLE_SIZE] = delta;
                    writeIndex++;
                    filled = Math.min(filled + 1, SAMPLE_SIZE);
                }
            }
            lastTickTime = now;
            if (filled > 0) {
                long sum = 0;
                int count = Math.min(filled, SAMPLE_SIZE);
                for (int i = 0; i < count; i++) {
                    sum += tickIntervals[i];
                }
                double avgMs = (double) sum / count;
                smoothedTps = Math.min(20.0, 1000.0 / avgMs);
            }
        });
    }

    public static double getTps() {
        return smoothedTps;
    }
}
