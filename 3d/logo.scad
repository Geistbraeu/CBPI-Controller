// --- НАСТРОЙКИ ФАЙЛОВ ---
file_frame      = "logo_frame_text.svg";      
file_center_log = "logo_log.svg";        
file_silhouette = "logo_silhouette.svg"; 

// --- ГЕОМЕТРИЯ ---
total_height      = 140;   
center_scale      = 0.45;
outline_thickness = 0.8;   // Тонкая аккуратная рамка

// --- ПОЗИЦИОНИРОВАНИЕ ---
// Если логотип смещен, меняй эти цифры:
offset_x = -10;  // Смещение влево/вправо
offset_y = 3;   // Смещение вверх/вниз

base_t = 2; 
logo_t = 2; 

$fn = 100;
c_h = total_height * center_scale;

// --- СБОРКА ---

// 1. ОСНОВАНИЕ (Овал)
color("brown")
linear_extrude(height = base_t) {
    scale([0.84, 1, 1]) circle(d = total_height + 4, $fn = 200);
}

translate([0, 0, base_t]) {

    // 2. ВНЕШНЯЯ РАМКА И ТЕКСТ
    color("Silver")
    linear_extrude(height = logo_t)
        resize([0, total_height, 0], auto=true)
            import(file_frame, center=true);

    // 3. ЦЕНТРАЛЬНАЯ ЭМБЛЕМА (С управлением позицией)
    
    translate([offset_x, offset_y, 0]) { // ТУТ МЫ ЦЕНТРИРУЕМ
        difference() {
            // А) ВЫПУКЛЫЙ СИЛУЭТ
            color("lightgray")
            linear_extrude(height = logo_t)
                offset(r = outline_thickness, $fn = 60) 
                    resize([0, c_h*1.1, 0], auto=true)
                        import(file_silhouette, center=true);
            
            // Б) ВЫРЕЗАЕМ ДЕТАЛИ (глаза и кирпичи)
            // Вырез на глубину 1.5мм (logo_t - 1.5)
            color("yellow")
            translate([0, 0, 1.5]) 
                linear_extrude(height = 2)
                    resize([0, c_h*1.1, 0], auto=true)
                        import(file_center_log, center=true);
        }
    }
}