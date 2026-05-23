package com.utilityclient.client.gui;

import net.minecraft.ChatFormatting;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.multiplayer.JoinMultiplayerScreen;
import net.minecraft.client.gui.screens.options.OptionsScreen;
import net.minecraft.client.gui.screens.worldselection.SelectWorldScreen;
import net.minecraft.network.chat.Component;

public final class SolarisScreen extends Screen {

    private static final int ACCENT  = 0xFFFF8C00;
    private static final int ACCENT2 = 0xFFFFBB44;
    private static final int BG_TOP  = 0xFF07070F;
    private static final int BG_BOT  = 0xFF111128;
    private static final int DIM     = 0xFF556688;

    private static final int BTN_W = 280;
    private static final int BTN_H = 22;
    private static final int BTN_GAP = 28;

    public SolarisScreen() {
        super(Component.literal("Solaris"));
    }

    @Override
    protected void init() {
        int cx  = width / 2;
        int by  = height / 2 + 8;

        addRenderableWidget(Button.builder(
            Component.literal("SINGLEPLAYER"),
            btn -> minecraft.setScreen(new SelectWorldScreen(this))
        ).pos(cx - BTN_W / 2, by).size(BTN_W, BTN_H).build());

        addRenderableWidget(Button.builder(
            Component.literal("MULTIPLAYER"),
            btn -> minecraft.setScreen(new JoinMultiplayerScreen(this))
        ).pos(cx - BTN_W / 2, by + BTN_GAP).size(BTN_W, BTN_H).build());

        int half = BTN_W / 2 - 2;
        addRenderableWidget(Button.builder(
            Component.literal("OPTIONS"),
            btn -> minecraft.setScreen(new OptionsScreen(this, minecraft.options))
        ).pos(cx - BTN_W / 2, by + BTN_GAP * 2).size(half, BTN_H).build());

        addRenderableWidget(Button.builder(
            Component.literal("QUIT"),
            btn -> minecraft.stop()
        ).pos(cx + 2, by + BTN_GAP * 2).size(half, BTN_H).build());
    }

    @Override
    public void render(GuiGraphics g, int mx, int my, float pt) {
        // Dark space background
        g.fillGradient(0, 0, width, height, BG_TOP, BG_BOT);

        // Subtle star-field dots
        drawStars(g);

        // Bottom accent bar
        g.fill(0, height - 20, width, height - 19, 0x66FF8C00);
        g.fillGradient(0, height - 19, width, height, 0x33FF8C00, 0x00000000);

        int cx    = width / 2;
        int logoY = height / 2 - 105;

        // Sun symbol
        drawSun(g, cx, logoY + 30, 26);

        // SOLARIS title — draw twice offset for a glow/depth effect
        g.drawCenteredString(font, Component.literal("SOLARIS").withStyle(ChatFormatting.BOLD), cx + 1, logoY + 67, 0x55FF6600);
        g.drawCenteredString(font, Component.literal("SOLARIS").withStyle(ChatFormatting.BOLD), cx,     logoY + 66, ACCENT);

        // Subtitle
        g.drawCenteredString(font, Component.literal("C L I E N T"), cx, logoY + 80, ACCENT2);

        // Thin divider under subtitle
        g.fill(cx - 50, logoY + 91, cx + 50, logoY + 92, 0x44FF8C00);

        // Bottom watermarks
        g.drawString(font, "Solaris 0.2.0  •  Minecraft 1.21.11", 5, height - 11, DIM, false);
        String copy = "Copyright Mojang Studios";
        g.drawString(font, copy, width - font.width(copy) - 5, height - 11, DIM, false);

        super.render(g, mx, my, pt);
    }

    private void drawSun(GuiGraphics g, int cx, int cy, int r) {
        // Core glow (outer soft ring)
        int core = r / 3;
        g.fill(cx - core - 2, cy - core - 2, cx + core + 2, cy + core + 2, 0x33FF8C00);
        // Core
        g.fill(cx - core, cy - core, cx + core, cy + core, ACCENT);
        // Bright center
        g.fill(cx - 1, cy - 1, cx + 1, cy + 1, 0xFFFFEE88);

        // Cardinal rays
        int gap = core + 3;
        g.fill(cx - 1, cy - r,   cx + 1, cy - gap, ACCENT2);
        g.fill(cx - 1, cy + gap, cx + 1, cy + r,   ACCENT2);
        g.fill(cx - r,   cy - 1, cx - gap, cy + 1, ACCENT2);
        g.fill(cx + gap, cy - 1, cx + r,   cy + 1, ACCENT2);

        // Diagonal rays (pixel dots fading out)
        for (int i = 0; i < 5; i++) {
            int s = gap + i * 3;
            int alpha = Math.max(0x20, 0xAA - i * 0x1C);
            int col = (alpha << 24) | 0xFFBB44;
            g.fill(cx + s,     cy - s - 1, cx + s + 2, cy - s + 1, col);
            g.fill(cx - s - 2, cy - s - 1, cx - s,     cy - s + 1, col);
            g.fill(cx + s,     cy + s - 1, cx + s + 2, cy + s + 1, col);
            g.fill(cx - s - 2, cy + s - 1, cx - s,     cy + s + 1, col);
        }
    }

    private void drawStars(GuiGraphics g) {
        // Deterministic pseudo-random star positions
        int[] seeds = {17, 31, 47, 59, 71, 89, 103, 127, 149, 163,
                       179, 197, 211, 233, 251, 269, 283, 307, 331, 349};
        for (int i = 0; i < seeds.length; i++) {
            int sx = (seeds[i] * 73 + i * 137) % Math.max(1, width);
            int sy = (seeds[i] * 41 + i * 59)  % Math.max(1, height / 2);
            int brightness = 0x44 + (i % 3) * 0x22;
            int col = (brightness << 24) | 0xCCDDFF;
            g.fill(sx, sy, sx + 1, sy + 1, col);
        }
    }

    @Override
    public boolean shouldCloseOnEsc() { return false; }

    @Override
    public boolean isPauseScreen() { return false; }
}
