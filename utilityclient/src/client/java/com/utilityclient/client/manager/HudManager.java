package com.utilityclient.client.manager;

import com.utilityclient.client.hud.HudModule;
import com.utilityclient.client.module.Module;
import java.util.ArrayList;
import java.util.List;

public final class HudManager {
    public List<HudModule> getHudModules(List<Module> allModules) {
        List<HudModule> modules = new ArrayList<>();
        for (Module module : allModules) {
            if (module instanceof HudModule hudModule) {
                modules.add(hudModule);
            }
        }
        return modules;
    }
}
