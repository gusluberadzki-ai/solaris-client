package com.utilityclient.client.util;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;

public final class RenderUtil {
    private RenderUtil() {
    }

    public static void panel(GuiGraphics graphics, int x, int y, int width, int height) {
        graphics.fill(x, y, x + width, y + height, 0xAA1F2937);
        graphics.fill(x, y, x + width, y + 1, 0xFF3B82F6);
        graphics.fill(x, y, x + 1, y + height, 0x663B82F6);
    }

    public static void outlinedBox(GuiGraphics graphics, int x, int y, int width, int height, int color) {
        graphics.renderOutline(x, y, width, height, color);
    }

    public static void text(GuiGraphics graphics, String text, int x, int y, int color) {
        Font font = Minecraft.getInstance().font;
        graphics.drawString(font, text, x, y, color, true);
    }

    public static void centered(GuiGraphics graphics, Component text, int centerX, int y, int color) {
        Font font = Minecraft.getInstance().font;
        graphics.drawCenteredString(font, text, centerX, y, color);
    }

    public static int durabilityColor(double percent) {
        if (percent > 0.6) {
            return 0xFF10B981;
        }
        if (percent > 0.3) {
            return 0xFFFBBF24;
        }
        return 0xFFEF4444;
    }
}
