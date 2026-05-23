package com.utilityclient.client.gui;

import com.utilityclient.client.UtilityClientClient;
import com.utilityclient.client.hud.HudModule;
import com.utilityclient.client.util.RenderUtil;
import java.util.List;
import net.minecraft.client.input.MouseButtonEvent;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;

public final class HudEditorScreen extends Screen {
    private HudModule dragging;
    private int dragOffsetX;
    private int dragOffsetY;

    public HudEditorScreen() {
        super(Component.literal("HUD Editor"));
    }

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        graphics.fill(0, 0, width, height, 0x80000000);
        List<HudModule> modules = UtilityClientClient.hudManager.getHudModules(UtilityClientClient.moduleManager.getModules());
        for (HudModule module : modules) {
            RenderUtil.panel(graphics, module.getX(), module.getY(), module.getWidth(), module.getHeight());
            RenderUtil.outlinedBox(graphics, module.getX(), module.getY(), module.getWidth(), module.getHeight(), 0xFF3B82F6);
            RenderUtil.text(graphics, module.getName(), module.getX() + 6, module.getY() + 6, 0xFFFFFFFF);
        }
        RenderUtil.centered(graphics, Component.literal("Drag HUD widgets. Positions save on close."), width / 2, 12, 0xFFFFFFFF);
        super.render(graphics, mouseX, mouseY, partialTick);
    }

    @Override
    public boolean mouseClicked(MouseButtonEvent event, boolean doubleClick) {
        for (HudModule module : UtilityClientClient.hudManager.getHudModules(UtilityClientClient.moduleManager.getModules())) {
            if (inside(module, event.x(), event.y())) {
                dragging = module;
                dragOffsetX = (int) event.x() - module.getX();
                dragOffsetY = (int) event.y() - module.getY();
                return true;
            }
        }
        return super.mouseClicked(event, doubleClick);
    }

    @Override
    public boolean mouseDragged(MouseButtonEvent event, double dragX, double dragY) {
        if (dragging != null) {
            dragging.setPosition((int) event.x() - dragOffsetX, (int) event.y() - dragOffsetY);
            return true;
        }
        return super.mouseDragged(event, dragX, dragY);
    }

    @Override
    public boolean mouseReleased(MouseButtonEvent event) {
        dragging = null;
        UtilityClientClient.configManager.saveAll();
        return super.mouseReleased(event);
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    private boolean inside(HudModule module, double mouseX, double mouseY) {
        return mouseX >= module.getX()
            && mouseX <= module.getX() + module.getWidth()
            && mouseY >= module.getY()
            && mouseY <= module.getY() + module.getHeight();
    }
}
