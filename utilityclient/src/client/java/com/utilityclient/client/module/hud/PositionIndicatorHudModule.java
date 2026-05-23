package com.utilityclient.client.module.hud;

import com.utilityclient.client.hud.HudModule;
import com.utilityclient.client.module.Category;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.setting.IntegerSetting;
import com.utilityclient.client.util.RenderUtil;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;

public final class PositionIndicatorHudModule extends HudModule {
    private final BooleanSetting showBiome = addSetting(new BooleanSetting("showBiome", "Display biome", true));
    private final BooleanSetting showDimension = addSetting(new BooleanSetting("showDimension", "Display dimension", true));
    private final BooleanSetting showNetherCoords = addSetting(new BooleanSetting("showNetherCoords", "Display converted coords", true));
    private final IntegerSetting decimalPlaces = addSetting(new IntegerSetting("decimalPlaces", "Coordinate precision", 2, 0, 4));

    public PositionIndicatorHudModule(KeyMapping keybind) {
        super("Position Indicator HUD", "Coordinates, direction, biome, and dimension.", Category.HUD, keybind, 12, 140);
        width = 185;
        height = 58;
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
        if (!isVisible() || client.player == null || client.level == null) {
            return;
        }
        BlockPos pos = client.player.blockPosition();
        String format = "%." + decimalPlaces.get() + "f";
        RenderUtil.panel(graphics, getX(), getY(), width, height);
        RenderUtil.text(graphics,
            "XYZ: " + String.format(format, client.player.getX())
                + ", " + String.format(format, client.player.getY())
                + ", " + String.format(format, client.player.getZ()),
            getX() + 6, getY() + 6, 0xFFFFFFFF);
        RenderUtil.text(graphics,
            "Facing: " + client.player.getDirection().getName()
                + " (" + String.format("%.1f", client.player.getYRot()) + ")",
            getX() + 6, getY() + 18, 0xFF93C5FD);
        int lineY = getY() + 30;

        if (showBiome.get()) {
            RenderUtil.text(graphics, "Biome: " + biomeName(client, pos), getX() + 6, lineY, 0xFF10B981);
            lineY += 12;
        }
        if (showDimension.get()) {
            RenderUtil.text(graphics, "Dim: " + dimensionName(client), getX() + 6, lineY, 0xFFFFFFFF);
            lineY += 12;
        }
        if (showNetherCoords.get()) {
            double scale = Level.NETHER.equals(client.level.dimension()) ? 8.0D : 0.125D;
            RenderUtil.text(graphics,
                String.format("Conv: %.1f, %.1f", client.player.getX() * scale, client.player.getZ() * scale),
                getX() + 6, lineY, 0xFFFBBF24);
            height = 66;
        } else {
            height = Math.max(42, lineY - getY());
        }
    }

    private static String biomeName(Minecraft client, BlockPos pos) {
        try {
            return client.level.getBiome(pos).unwrapKey()
                .map(k -> k.identifier().getPath().replace('_', ' '))
                .orElse("unknown");
        } catch (Exception e) {
            return "unknown";
        }
    }

    private static String dimensionName(Minecraft client) {
        var dim = client.level.dimension();
        if (Level.OVERWORLD.equals(dim)) return "Overworld";
        if (Level.NETHER.equals(dim))    return "Nether";
        if (Level.END.equals(dim))       return "End";
        // Modded dimension: parse "ResourceKey[... / namespace:path]" → "path"
        String raw = dim.toString();
        int slash = raw.lastIndexOf('/');
        if (slash >= 0 && raw.endsWith("]")) {
            return raw.substring(slash + 2, raw.length() - 1);
        }
        return raw;
    }
}
