package com.utilityclient.client.hud;

import com.utilityclient.client.module.Category;
import com.utilityclient.client.module.Module;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.setting.IntegerSetting;
import net.minecraft.client.KeyMapping;

public abstract class HudModule extends Module {
    protected final IntegerSetting x;
    protected final IntegerSetting y;
    protected final BooleanSetting visible;
    protected int width = 120;
    protected int height = 40;

    protected HudModule(String name, String description, Category category, KeyMapping keybind, int x, int y) {
        super(name, description, category, keybind);
        this.x = addSetting(new IntegerSetting("x", "Horizontal position", x, 0, 6000));
        this.y = addSetting(new IntegerSetting("y", "Vertical position", y, 0, 6000));
        this.visible = addSetting(new BooleanSetting("visible", "Whether the HUD is drawn", true));
    }

    public int getX() {
        return x.get();
    }

    public int getY() {
        return y.get();
    }

    public void setPosition(int x, int y) {
        this.x.set(x);
        this.y.set(y);
    }

    public boolean isVisible() {
        return visible.get();
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }
}
