package com.friday.rpg.inventory;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class Inventory implements Serializable {
    private static final long serialVersionUID = 1L;
    
    private int maxSize;
    private List<ItemSlot> items;
    
    public Inventory(int maxSize) {
        this.maxSize = maxSize;
        this.items = new ArrayList<>();
    }
    
    public boolean addItem(Item item) {
        if (isFull()) return false;
        
        if (item.getType() == Item.ItemType.CONSUMABLE || item.getType() == Item.ItemType.MATERIAL) {
            for (ItemSlot slot : items) {
                if (slot.getItem().getId().equals(item.getId()) && slot.getQuantity() < 99) {
                    slot.addQuantity(1);
                    return true;
                }
            }
        }
        
        items.add(new ItemSlot(item, 1));
        return true;
    }
    
    public boolean removeItem(Item item) {
        for (ItemSlot slot : items) {
            if (slot.getItem().getId().equals(item.getId())) {
                slot.removeQuantity(1);
                if (slot.getQuantity() <= 0) items.remove(slot);
                return true;
            }
        }
        return false;
    }
    
    public Item getItemAt(int index) {
        if (index >= 0 && index < items.size()) return items.get(index).getItem();
        return null;
    }
    
    public List<ItemSlot> getAllSlots() { return new ArrayList<>(items); }
    public int getSize() { return items.size(); }
    public int getMaxSize() { return maxSize; }
    public boolean isFull() { return items.size() >= maxSize; }
    public boolean isEmpty() { return items.isEmpty(); }
    
    public static class ItemSlot implements Serializable {
        private Item item;
        private int quantity;
        
        public ItemSlot(Item item, int quantity) {
            this.item = item;
            this.quantity = quantity;
        }
        
        public Item getItem() { return item; }
        public int getQuantity() { return quantity; }
        public void addQuantity(int amount) { this.quantity += amount; }
        public void removeQuantity(int amount) { this.quantity -= amount; }
    }
}
