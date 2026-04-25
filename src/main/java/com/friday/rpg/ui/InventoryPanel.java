package com.friday.rpg.ui;

import com.friday.rpg.core.GameState;
import com.friday.rpg.core.Player;
import com.friday.rpg.inventory.Equipment;
import com.friday.rpg.inventory.Inventory;
import com.friday.rpg.inventory.Item;
import javafx.geometry.Insets;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.ScrollPane;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;

public class InventoryPanel extends VBox {
    
    private GameState gameState;
    private GridPane equipSlots;
    private VBox inventoryList;
    
    public InventoryPanel(GameState gameState) {
        this.gameState = gameState;
        setSpacing(10);
        setPadding(new Insets(10));
        
        Label title = new Label("INVENTORY");
        title.setFont(Font.font(GameWindow.FONT_FAMILY, FontWeight.BOLD, 14));
        title.setTextFill(Color.web("#00ff41"));
        
        equipSlots = createEquipSlots();
        inventoryList = new VBox(2);
        
        ScrollPane scrollPane = new ScrollPane(inventoryList);
        scrollPane.setFitToWidth(true);
        scrollPane.setPrefHeight(200);
        scrollPane.setStyle("-fx-background: #0a0a0a; -fx-border-color: #00ff41; -fx-border-width: 1;");
        
        getChildren().addAll(title, equipSlots, scrollPane);
        VBox.setVgrow(scrollPane, Priority.ALWAYS);
    }
    
    private GridPane createEquipSlots() {
        GridPane grid = new GridPane();
        grid.setHgap(8);
        grid.setVgap(8);
        
        String[] slots = {"WPN", "ARM", "HLM", "ACC1", "ACC2"};
        String[] icons = {"⚔", "⛨", "⛑", "◈", "◈"};
        
        for (int i = 0; i < 5; i++) {
            Button slot = new Button(icons[i] + "\n" + slots[i]);
            slot.setFont(Font.font(GameWindow.FONT_FAMILY, 10));
            slot.setStyle("-fx-background-color: transparent; -fx-text-fill: #00ff41; -fx-border-color: #00ff41; -fx-min-width: 60; -fx-min-height: 60;");
            grid.add(slot, i % 3, i / 3);
        }
        
        return grid;
    }
    
    public void setGameState(GameState gameState) {
        this.gameState = gameState;
        update();
    }
    
    public void update() {
        if (gameState == null || gameState.getPlayer() == null) return;
        
        Player player = gameState.getPlayer();
        Inventory inv = player.getInventory();
        
        inventoryList.getChildren().clear();
        
        for (Inventory.ItemSlot slot : inv.getAllSlots()) {
            Item item = slot.getItem();
            int qty = slot.getQuantity();
            
            HBox row = new HBox(10);
            row.setPadding(new Insets(5));
            row.setStyle("-fx-border-color: #1a1a1a; -fx-border-width: 1;");
            
            Label icon = new Label(item.getIcon());
            icon.setFont(Font.font(16));
            icon.setTextFill(getRarityColor(item.getRarity()));
            
            Label name = new Label(item.getName() + (qty > 1 ? " x" + qty : ""));
            name.setFont(Font.font(GameWindow.FONT_FAMILY, 11));
            name.setTextFill(getRarityColor(item.getRarity()));
            
            row.getChildren().addAll(icon, name);
            inventoryList.getChildren().add(row);
        }
        
        if (inventoryList.getChildren().isEmpty()) {
            Label empty = new Label("(Empty)");
            empty.setFont(Font.font(GameWindow.FONT_FAMILY, 10));
            empty.setTextFill(Color.web("#444444"));
            inventoryList.getChildren().add(empty);
        }
    }
    
    private Color getRarityColor(Item.ItemRarity rarity) {
        switch (rarity) {
            case COMMON: return Color.web("#ffffff");
            case UNCOMMON: return Color.web("#00ff00");
            case RARE: return Color.web("#0088ff");
            case EPIC: return Color.web("#aa00ff");
            case LEGENDARY: return Color.web("#ffaa00");
            default: return Color.web("#ffffff");
        }
    }
}
