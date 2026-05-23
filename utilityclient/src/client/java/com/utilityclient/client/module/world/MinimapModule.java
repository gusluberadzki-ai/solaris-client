package com.utilityclient.client.module.world;

import com.utilityclient.client.hud.HudModule;
import com.utilityclient.client.module.Category;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.setting.EnumSetting;
import com.utilityclient.client.setting.IntegerSetting;
import com.utilityclient.client.util.RenderUtil;
import java.util.concurrent.ConcurrentHashMap;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.core.BlockPos;

public final class MinimapModule extends HudModule {
    public enum Shape {
        SQUARE,
        CIRCLE
    }

    private final IntegerSetting size = addSetting(new IntegerSetting("size", "Map size in pixels", 96, 64, 220));
    private final IntegerSetting zoom = addSetting(new IntegerSetting("zoom", "Chunk sample radius", 6, 2, 16));
    private final EnumSetting<Shape> shape = addSetting(new EnumSetting<>("shape", "Map shape", Shape.SQUARE, Shape.class));
    private final BooleanSetting showPlayers = addSetting(new BooleanSetting("showPlayers", "Show nearby players", true));
    private final BooleanSetting showWaypoints = addSetting(new BooleanSetting("showWaypoints", "Show waypoint markers", true));
    private final BooleanSetting rotate = addSetting(new BooleanSetting("rotate", "Rotate with player yaw", true));
    private final ConcurrentHashMap<Long, Integer> chunkColorCache = new ConcurrentHashMap<>();

    public MinimapModule(KeyMapping keybind) {
        super("Minimap", "Corner minimap with chunk cache scaffolding.", Category.WORLD, keybind, 410, 110);
        width = 104;
        height = 104;
        setEnabledSilently(true);
    }

    @Override
    public void onEnable() {
    }

    @Override
    public void onDisable() {
    }

    @Override
    public void onHudRender(GuiGraphics graphics, float tickDelta) {
        Minecraft client = Minecraft.getInstance();
        if (!isVisible() || client.player == null) {
            return;
        }
        width = size.get();
        height = size.get();
        RenderUtil.panel(graphics, getX(), getY(), width, height);
        int samples = Math.max(8, zoom.get() * 2);
        int cell = Math.max(2, width / samples);
        BlockPos origin = client.player.blockPosition();
        for (int gx = 0; gx < samples; gx++) {
            for (int gz = 0; gz < samples; gz++) {
                int worldX = origin.getX() + (gx - samples / 2) * 4;
                int worldZ = origin.getZ() + (gz - samples / 2) * 4;
                long key = (((long) worldX) << 32) ^ worldZ;
                int color = chunkColorCache.computeIfAbsent(key, ignored -> sampleColor(worldX, worldZ));
                graphics.fill(getX() + gx * cell, getY() + gz * cell, getX() + (gx + 1) * cell, getY() + (gz + 1) * cell, color);
            }
        }
        graphics.fill(getX() + width / 2 - 2, getY() + height / 2 - 2, getX() + width / 2 + 2, getY() + height / 2 + 2, 0xFFFFFFFF);
        RenderUtil.text(graphics, shape.get().name() + (rotate.get() ? " R" : ""), getX() + 4, getY() + 4, 0xFFFFFFFF);
        if (showPlayers.get()) {
            RenderUtil.text(graphics, "P", getX() + width - 12, getY() + 4, 0xFF93C5FD);
        }
        if (showWaypoints.get()) {
            RenderUtil.text(graphics, "W", getX() + width - 24, getY() + 4, 0xFF10B981);
        }
    }

    private int sampleColor(int worldX, int worldZ) {
        int hash = Math.abs((worldX * 734287 + worldZ * 912271) ^ 0x334455);
        int green = 90 + (hash % 100);
        int blue = 60 + (hash / 13 % 70);
        return 0xFF000000 | (40 << 16) | (green << 8) | blue;
    }
}
