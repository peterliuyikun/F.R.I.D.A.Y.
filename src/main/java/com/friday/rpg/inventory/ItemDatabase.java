package com.friday.rpg.inventory;

import java.util.*;

public class ItemDatabase {
    private static final Map<String, Item> items = new HashMap<>();
    private static final Random random = new Random();
    
    static {
        initializeItems();
    }
    
    private static void initializeItems() {
        // Weapons
        register(new Item("wep_001", "Vibroblade", Item.ItemType.WEAPON, Item.ItemRarity.COMMON)
            .withDescription("A standard vibroblade weapon")
            .withStats(5, 0, 0, 0, 0).withValue(50));
        
        register(new Item("wep_002", "Plasma Sword", Item.ItemType.WEAPON, Item.ItemRarity.UNCOMMON)
            .withDescription("Blade heated by plasma")
            .withStats(8, 0, 0, 0, 2).withValue(150));
        
        register(new Item("wep_003", "Lightsaber", Item.ItemType.WEAPON, Item.ItemRarity.EPIC)
            .withDescription("The weapon of a Jedi or Sith")
            .withStats(15, 0, 10, 0, 5).withValue(1000));
        
        // Armor
        register(new Item("arm_001", "Combat Vest", Item.ItemType.ARMOR, Item.ItemRarity.COMMON)
            .withDescription("Basic protective vest")
            .withStats(0, 5, 0, 0, 0).withValue(60));
        
        register(new Item("arm_002", "Battle Armor", Item.ItemType.ARMOR, Item.ItemRarity.UNCOMMON)
            .withDescription("Reinforced battle armor")
            .withStats(0, 10, 0, 2, -1).withValue(200));
        
        register(new Item("arm_003", "Mandalorian Armor", Item.ItemType.ARMOR, Item.ItemRarity.RARE)
            .withDescription("Armor forged by Mandalorian smiths")
            .withStats(2, 15, 0, 5, 0).withValue(800));
        
        // Helmets
        register(new Item("hlm_001", "Combat Helmet", Item.ItemType.HELMET, Item.ItemRarity.COMMON)
            .withDescription("Standard issue helmet")
            .withStats(0, 3, 0, 0, 0).withValue(40));
        
        // Accessories
        register(new Item("acc_001", "Strength Amulet", Item.ItemType.ACCESSORY, Item.ItemRarity.UNCOMMON)
            .withDescription("Enhances physical strength")
            .withStats(3, 0, 0, 0, 0).withValue(100));
        
        // Consumables
        register(new Item("cns_001", "Medpac", Item.ItemType.CONSUMABLE, Item.ItemRarity.COMMON)
            .withDescription("Restores health").withValue(25));
        
        register(new Item("cns_002", "Advanced Medpac", Item.ItemType.CONSUMABLE, Item.ItemRarity.UNCOMMON)
            .withDescription("Restores significant health").withValue(75));
        
        register(new Item("cns_003", "Force Potion", Item.ItemType.CONSUMABLE, Item.ItemRarity.RARE)
            .withDescription("Restores Force energy").withValue(100));
    }
    
    private static void register(Item item) {
        items.put(item.getId(), item);
    }
    
    public static Item get(String id) {
        return items.get(id);
    }
    
    public static Item getRandomEquipment(int level) {
        List<Item> equipment = new ArrayList<>();
        for (Item item : items.values()) {
            if (item.getType() != Item.ItemType.CONSUMABLE && item.getType() != Item.ItemType.MATERIAL) {
                equipment.add(item);
            }
        }
        return equipment.get(random.nextInt(equipment.size()));
    }
    
    public static Item getRandomConsumable(int level) {
        List<Item> consumables = new ArrayList<>();
        for (Item item : items.values()) {
            if (item.getType() == Item.ItemType.CONSUMABLE) {
                consumables.add(item);
            }
        }
        return consumables.get(random.nextInt(consumables.size()));
    }
}
