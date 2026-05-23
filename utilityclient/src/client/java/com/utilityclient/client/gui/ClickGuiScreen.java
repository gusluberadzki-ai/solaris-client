package com.utilityclient.client.gui;

import com.utilityclient.client.UtilityClientClient;
import com.utilityclient.client.module.Category;
import com.utilityclient.client.module.Module;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.setting.ColorSetting;
import com.utilityclient.client.setting.DoubleSetting;
import com.utilityclient.client.setting.EnumSetting;
import com.utilityclient.client.setting.IntegerSetting;
import com.utilityclient.client.setting.Setting;
import com.utilityclient.client.setting.StringSetting;
import com.utilityclient.client.util.RenderUtil;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;

public final class ClickGuiScreen extends Screen {
    private enum ViewTab {
        MODULES,
        SETTINGS
    }

    private Category selectedCategory = Category.HUD;
    private Module selectedModule;
    private ViewTab activeTab = ViewTab.MODULES;

    public ClickGuiScreen() {
        super(Component.literal("Utility Client"));
    }

    @Override
    protected void init() {
        if (selectedModule == null) {
            selectedModule = UtilityClientClient.moduleManager.getByCategory(selectedCategory).stream().findFirst().orElse(null);
        }
        rebuildWidgets();
    }

    @Override
    protected void rebuildWidgets() {
        clearWidgets();

        addRenderableWidget(Button.builder(Component.translatable("screen.utilityclient.modules"), button -> {
            activeTab = ViewTab.MODULES;
            rebuildWidgets();
        }).pos(24, 20).size(110, 20).build());

        addRenderableWidget(Button.builder(Component.translatable("screen.utilityclient.settings"), button -> {
            activeTab = ViewTab.SETTINGS;
            rebuildWidgets();
        }).pos(140, 20).size(110, 20).build());

        int categoryX = 24;
        int y = 52;
        for (Category category : Category.values()) {
            addRenderableWidget(Button.builder(Component.literal(prefix(category == selectedCategory) + category.getDisplayName()), button -> {
                selectedCategory = category;
                if (selectedModule == null || selectedModule.getCategory() != category) {
                    selectedModule = UtilityClientClient.moduleManager.getByCategory(category).stream().findFirst().orElse(null);
                }
                rebuildWidgets();
            }).pos(categoryX, y).size(140, 20).build());
            y += 24;
        }

        buildModuleButtons();
        if (activeTab == ViewTab.SETTINGS) {
            buildSettingsButtons();
        }
    }

    private void buildModuleButtons() {
        int moduleX = 184;
        int y = 52;
        for (Module module : UtilityClientClient.moduleManager.getByCategory(selectedCategory)) {
            addRenderableWidget(Button.builder(Component.literal(moduleLabel(module)), button -> {
                if (activeTab == ViewTab.MODULES) {
                    module.toggle();
                }
                selectedModule = module;
                rebuildWidgets();
            }).pos(moduleX, y).size(210, 20).build());
            y += 24;
        }
    }

    private void buildSettingsButtons() {
        if (selectedModule == null) {
            return;
        }
        int settingX = 414;
        int y = 52;
        for (Setting<?> setting : selectedModule.getSettings()) {
            addRenderableWidget(Button.builder(Component.literal(settingLabel(setting)), button -> {
                mutateSetting(setting);
                UtilityClientClient.configManager.saveModule(selectedModule);
                rebuildWidgets();
            }).pos(settingX, y).size(220, 20).build());
            y += 24;
            if (y > height - 30) {
                break;
            }
        }
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    private void mutateSetting(Setting<?> setting) {
        if (setting instanceof BooleanSetting booleanSetting) {
            booleanSetting.set(!booleanSetting.get());
            return;
        }
        if (setting instanceof IntegerSetting integerSetting) {
            integerSetting.set(integerSetting.get() + 1);
            return;
        }
        if (setting instanceof DoubleSetting doubleSetting) {
            doubleSetting.set(doubleSetting.get() + 0.1D);
            return;
        }
        if (setting instanceof EnumSetting enumSetting) {
            Enum value = (Enum) enumSetting.get();
            Object[] values = value.getDeclaringClass().getEnumConstants();
            int nextIndex = (value.ordinal() + 1) % values.length;
            enumSetting.set((Enum) values[nextIndex]);
            return;
        }
        if (setting instanceof ColorSetting colorSetting) {
            List<int[]> palette = new ArrayList<>(Arrays.asList(
                new int[] {16, 185, 129, 255},
                new int[] {59, 130, 246, 255},
                new int[] {251, 191, 36, 255},
                new int[] {239, 68, 68, 255},
                new int[] {255, 255, 255, 255}
            ));
            int[] current = colorSetting.get();
            int index = 0;
            for (int i = 0; i < palette.size(); i++) {
                if (Arrays.equals(current, palette.get(i))) {
                    index = i;
                    break;
                }
            }
            colorSetting.set(palette.get((index + 1) % palette.size()));
            return;
        }
        if (setting instanceof StringSetting stringSetting) {
            stringSetting.set(stringSetting.get() + " *");
        }
    }

    private String prefix(boolean selected) {
        return selected ? "> " : "";
    }

    private String moduleLabel(Module module) {
        String selected = selectedModule == module ? "* " : "";
        return selected + (module.isEnabled() ? "[ON] " : "[OFF] ") + module.getName();
    }

    private String settingLabel(Setting<?> setting) {
        return setting.getName() + ": " + formatValue(setting.get());
    }

    private String formatValue(Object value) {
        if (value instanceof int[] rgba) {
            return rgba[0] + "," + rgba[1] + "," + rgba[2] + "," + rgba[3];
        }
        return String.valueOf(value);
    }

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        graphics.fill(0, 0, width, height, 0xC0101010);
        RenderUtil.panel(graphics, 16, 14, width - 32, height - 28);
        RenderUtil.centered(graphics, Component.literal("Utility Client"), width / 2, 20, 0xFFFFFFFF);
        RenderUtil.text(graphics, "Categories", 24, 42, 0xFF93C5FD);
        RenderUtil.text(graphics, "Modules", 184, 42, 0xFF93C5FD);
        RenderUtil.text(graphics, "Settings", 414, 42, 0xFF93C5FD);
        if (selectedModule != null) {
            RenderUtil.text(graphics, selectedModule.getDescription(), 414, height - 24, 0xFFFFFFFF);
        }
        super.render(graphics, mouseX, mouseY, partialTick);
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }
}
