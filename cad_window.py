from os import path

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence
from cad_widget import *
from cad_button import CADButton
from input_handler import handle_input
from cad_graphics_dot import *
from cad_graphics_line import *
from geometry import *

ICON_DIR = path.join(path.dirname(path.abspath(__file__)), 'icons')

CONSTRAINT_INFO = {
    1: ("Совпадение двух точек", "1.svg"),
    2: ("Расстояние между двумя точками", "2.svg"),
    3: ("Параллельность двух отрезков", "3.svg"),
    4: ("Перпендикулярность двух отрезков", "4.svg"),
    5: ("Вертикальность отрезка", "5.svg"),
    6: ("Горизонтальность отрезка", "6.svg"),
    7: ("Угол между двумя отрезками", "7.svg"),
    8: ("Принадлежность точки прямой", "8.svg"),
    9: ("Фиксация точки", "9.svg"),
}

class CADWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cad = None
        self.active_button = None
        self.coordinates_list = []
        self.constraints = []
        self.solver = Solver()
        self._syncing_selection = False
        self._object_items = {}
        self._object_graphics = {}

        self.initUI()

        self.set_background_palette("#2c3e50")

        # self.add_constraint("Расстояние", "Point_1", "Point_2")


    def initUI(self):

        self.load_styles()

        # СОЗДАНИЕ ДОКА С ОБЪЕКТАМИ И ОГРАНИЧЕНИЯМИ
        self.constraints_dock = QDockWidget("Построение", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.constraints_dock)
        self.constraints_dock.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.constraints_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.constraints_dock.toggleViewAction().setEnabled(False)

        build_container = QWidget()
        build_layout = QVBoxLayout(build_container)
        build_layout.setContentsMargins(4, 4, 4, 4)
        build_layout.setSpacing(4)

        objects_label = QLabel("Объекты")
        objects_label.setProperty("class", "panel-section")
        objects_label.style().unpolish(objects_label)
        objects_label.style().polish(objects_label)

        self.objects_list = QListWidget()
        self.objects_list.setAlternatingRowColors(True)
        self.objects_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        constraints_label = QLabel("Ограничения")
        constraints_label.setProperty("class", "panel-section")
        constraints_label.style().unpolish(constraints_label)
        constraints_label.style().polish(constraints_label)

        self.constraints_list = QListWidget()
        self.constraints_list.setAlternatingRowColors(True)
        self.constraints_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.constraints_list.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.constraints_list.customContextMenuRequested.connect(self.show_context_menu)

        build_layout.addWidget(objects_label)
        build_layout.addWidget(self.objects_list, 1)
        build_layout.addWidget(constraints_label)
        build_layout.addWidget(self.constraints_list, 1)

        self.constraints_dock.setWidget(build_container)


        # СОЗДАНИЕ ПАНЕЛИ С КНОПКАМИ
        buttons_toolbar = QToolBar("buttons", self)
        buttons_toolbar.setMovable(False)
        buttons_toolbar.setFloatable(False)
        buttons_toolbar.setAllowedAreas(Qt.TopToolBarArea)
        buttons_toolbar.toggleViewAction().setEnabled(False)
        self.addToolBar(Qt.TopToolBarArea, buttons_toolbar)

        title_widget = QWidget()
        groups_layout = QHBoxLayout(title_widget)
        groups_layout.setContentsMargins(4, 2, 4, 2)
        groups_layout.setSpacing(24)

        # СОЗДАНИЕ ТОЧЕК И ПРЯМЫХ
        self.btn1 = QPushButton("Add dot")
        self.btn1.setIcon(QIcon(f'{ICON_DIR}/dot.svg'))
        self.btn1.setIconSize(QSize(24, 24))

        # self.btn1.setProperty("class", "inactive")
        self.btn2 = QPushButton("Add line")
        self.btn2.setIcon(QIcon(f'{ICON_DIR}/line.svg'))
        self.btn2.setIconSize(QSize(24, 24))

        # ОГРАНИЧЕНИЯ
        # совпадение двух точек
        self.btn3 = QPushButton()
        self.btn3.setIcon(QIcon(f'{ICON_DIR}/1.svg'))
        self.btn3.setIconSize(QSize(24, 24))

        # расстояние между двумя точками
        self.btn5 = QPushButton()
        self.btn5.setIcon(QIcon(f'{ICON_DIR}/2.svg'))
        self.btn5.setIconSize(QSize(24, 24))

        # параллельность двух отрезков
        self.btn6 = QPushButton()
        self.btn6.setIcon(QIcon(f'{ICON_DIR}/3.svg'))
        self.btn6.setIconSize(QSize(24, 24))

        # перпендикулярность двух отрезков
        self.btn7 = QPushButton()
        self.btn7.setIcon(QIcon(f'{ICON_DIR}/4.svg'))
        self.btn7.setIconSize(QSize(24, 24))

        # вертикальность отрезка
        self.btn8 = QPushButton()
        self.btn8.setIcon(QIcon(f'{ICON_DIR}/5.svg'))
        self.btn8.setIconSize(QSize(24, 24))

        # горизонтальность отрезка
        self.btn9 = QPushButton()
        self.btn9.setIcon(QIcon(f'{ICON_DIR}/6.svg'))
        self.btn9.setIconSize(QSize(24, 24))

        # угол между отрезками
        self.btn10 = QPushButton()
        self.btn10.setIcon(QIcon(f'{ICON_DIR}/7.svg'))
        self.btn10.setIconSize(QSize(24, 24))

        # принадлежность точки прямой
        self.btn11 = QPushButton()
        self.btn11.setIcon(QIcon(f'{ICON_DIR}/8.svg'))
        self.btn11.setIconSize(QSize(24, 24))

        # фиксация точки
        self.btn12 = QPushButton()
        self.btn12.setIcon(QIcon(f'{ICON_DIR}/9.svg'))
        self.btn12.setIconSize(QSize(24, 24))

        tooltips = [
            (self.btn1, "Точка", "Создаёт точку в рабочей области по клику."),
            (self.btn2, "Отрезок", "Создаёт отрезок между двумя выбранными точками."),
            (self.btn3, "Совпадение точек", "Совмещает две выбранные точки в одну."),
            (self.btn5, "Расстояние", "Задаёт расстояние между двумя выбранными точками."),
            (self.btn6, "Параллельность", "Делает два выбранных отрезка параллельными."),
            (self.btn7, "Перпендикулярность", "Делает два выбранных отрезка перпендикулярными."),
            (self.btn8, "Вертикальность", "Фиксирует выбранный отрезок вертикально."),
            (self.btn9, "Горизонтальность", "Фиксирует выбранный отрезок горизонтально."),
            (self.btn10, "Угол", "Задаёт угол между двумя выбранными отрезками."),
            (self.btn11, "Точка на прямой", "Располагает выбранную точку на выбранном отрезке."),
            (self.btn12, "Фиксация точки", "Закрепляет выбранную точку в текущем положении."),
        ]
        for button, title, description in tooltips:
            button.setToolTip(f"<b>{title}</b><br>{description}")

        primitives_group = self._create_toolbar_group(
            "Геометрические примитивы",
            [self.btn1, self.btn2],
        )
        constraints_group = self._create_toolbar_group(
            "Геометрические ограничения",
            [
                self.btn3, self.btn5, self.btn6, self.btn7, self.btn8,
                self.btn9, self.btn10, self.btn11, self.btn12,
            ],
        )
        groups_layout.addWidget(primitives_group)
        groups_layout.addWidget(constraints_group)
        groups_layout.addStretch()

        buttons_toolbar.addWidget(title_widget)

        for btn in self.findChildren(QPushButton):
            self.apply_button_style(btn, "bla")

        # подключение кнопок
        self.btn1.clicked.connect(self.onButton1Clicked)
        self.btn2.clicked.connect(self.onButton2Clicked)
        self.btn3.clicked.connect(self.onButton3Clicked)
        self.btn5.clicked.connect(self.onButton5Clicked)
        self.btn6.clicked.connect(self.onButton6Clicked)
        self.btn7.clicked.connect(self.onButton7Clicked)
        self.btn8.clicked.connect(self.onButton8Clicked)
        self.btn9.clicked.connect(self.onButton9Clicked)
        self.btn10.clicked.connect(self.onButton10Clicked)
        self.btn11.clicked.connect(self.onButton11Clicked)
        self.btn12.clicked.connect(self.onButton12Clicked)

        self.delete_shortcut = QShortcut(QKeySequence(Qt.Key_Delete), self)
        self.delete_shortcut.activated.connect(self.delete_selected)

        
        self.cad = CadWidget(self.cad)
        self.setCentralWidget(self.cad)

        self.refresh_objects_list()
        self.refresh_constraints_list()

        self.objects_list.itemSelectionChanged.connect(
            self.on_objects_selection_changed
        )
        self.constraints_list.itemSelectionChanged.connect(
            self.on_constraints_selection_changed
        )

        # status bar
        # self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.status_mouse_pos.setStyleSheet("color: white;") 
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        self.cad.view.scenePosChanged.connect(self.onScenePosChanged)


        self.setGeometry(200, 200, 1000, 600)
        self.setWindowTitle("AutoAD")
        self.show()

    def _create_toolbar_group(self, title, buttons):
        group = QWidget()
        group_layout = QVBoxLayout(group)
        group_layout.setContentsMargins(0, 0, 0, 0)
        group_layout.setSpacing(2)

        label = QLabel(title)
        label.setProperty("class", "toolbar-section")
        label.style().unpolish(label)
        label.style().polish(label)
        group_layout.addWidget(label)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(4)
        for button in buttons:
            buttons_layout.addWidget(button)
        buttons_layout.addStretch()
        group_layout.addLayout(buttons_layout)

        return group

    def set_background_palette(self, color_name):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color_name))
        # palette.setBrush(QPalette.Window, QBrush(Qt.white, Qt.DiagCrossPattern))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def load_styles(self):
        """Загружает стили из файла"""
        try:
            with open('qss/style.qss', 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
                print("read")
        except FileNotFoundError:
            print("styles.qss не найден")


    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    # CONSTRAINTS LOGIC
    def constraint_exists(self, constraint_type, objects):
        return any(
            c["type"] == constraint_type and set(c["objects"]) == set(objects)
            for c in self.constraints
        )

    def _object_label(self, uuid):
        if self.cad is not None:
            if self.cad.scene.find_dot_by_uuid(uuid) is not None:
                return f"Точка {str(uuid)[:8]}"
            if self.cad.scene.find_line_by_uuid(uuid) is not None:
                return f"Отрезок {str(uuid)[:8]}"
        return f"Объект {str(uuid)[:8]}"

    def _constraint_name(self, constraint):
        name, _ = CONSTRAINT_INFO.get(
            constraint["type"],
            (f"Ограничение {constraint['type']}", None),
        )
        return name

    def _constraint_text(self, constraint):
        objects = " ↔ ".join(
            self._object_label(uuid) for uuid in constraint["objects"]
        )
        if objects:
            return f"{self._constraint_name(constraint)}: {objects}"
        return self._constraint_name(constraint)

    def refresh_objects_list(self):
        was_syncing = self._syncing_selection
        self._syncing_selection = True
        try:
            self.objects_list.clear()
            self._object_items.clear()
            self._object_graphics.clear()
            if self.cad is not None:
                for dot in self.cad.scene.dots:
                    item = QListWidgetItem(
                        QIcon(f'{ICON_DIR}/dot.svg'),
                        f"Точка {str(dot.uuid)[:8]}",
                    )
                    item.setData(Qt.UserRole, ("object", dot))
                    self.objects_list.addItem(item)
                    self._object_items[dot.uuid] = item
                    self._object_graphics[dot.uuid] = dot.grNode

                for line in self.cad.scene.lines:
                    item = QListWidgetItem(
                        QIcon(f'{ICON_DIR}/line.svg'),
                        f"Отрезок {str(line.uuid)[:8]}",
                    )
                    item.setData(Qt.UserRole, ("object", line))
                    self.objects_list.addItem(item)
                    self._object_items[line.uuid] = item
                    self._object_graphics[line.uuid] = line.grLine
        finally:
            self._syncing_selection = was_syncing
        self.sync_objects_selection_from_scene()

    def refresh_constraints_list(self):
        was_syncing = self._syncing_selection
        self._syncing_selection = True
        try:
            self.constraints_list.clear()
            for constraint in self.constraints:
                item = QListWidgetItem(self._constraint_text(constraint))
                icon_file = CONSTRAINT_INFO.get(constraint["type"], (None, None))[1]
                if icon_file is not None:
                    item.setIcon(QIcon(f'{ICON_DIR}/{icon_file}'))
                item.setData(Qt.UserRole, ("constraint", constraint))
                item.setToolTip(
                    ", ".join(str(uuid) for uuid in constraint["objects"])
                )
                self.constraints_list.addItem(item)
        finally:
            self._syncing_selection = was_syncing
        self._clear_constraint_highlight()

    def sync_objects_selection_from_scene(self):
        if self._syncing_selection or self.cad is None:
            return

        self._syncing_selection = True
        try:
            self.objects_list.clearSelection()
            for item in self.cad.scene.grScene.selectedItems():
                uuid = getattr(item, "uuid", None)
                list_item = self._object_items.get(uuid)
                if list_item is not None:
                    list_item.setSelected(True)
                    self.objects_list.scrollToItem(list_item)
            self.constraints_list.clearSelection()
            self._clear_constraint_highlight()
        finally:
            self._syncing_selection = False

    def on_objects_selection_changed(self):
        if self._syncing_selection or self.cad is None:
            return

        self._syncing_selection = True
        try:
            selected_uuids = set()
            for item in self.objects_list.selectedItems():
                data = item.data(Qt.UserRole)
                if data is not None and data[0] == "object":
                    selected_uuids.add(data[1].uuid)

            gr_scene = self.cad.scene.grScene
            gr_scene.clearSelection()
            for uuid in selected_uuids:
                gr_item = self._object_graphics.get(uuid)
                if gr_item is not None:
                    gr_item.setSelected(True)
            gr_scene.update()

            self.constraints_list.clearSelection()
            self._clear_constraint_highlight()
        finally:
            self._syncing_selection = False

    def on_constraints_selection_changed(self):
        if self._syncing_selection or self.cad is None:
            return

        self._syncing_selection = True
        try:
            self.objects_list.clearSelection()
            self.cad.scene.grScene.clearSelection()
            self.cad.scene.grScene.update()
        finally:
            self._syncing_selection = False
        self._apply_constraint_highlight()

    def _clear_constraint_highlight(self):
        for gr_item in self._object_graphics.values():
            if hasattr(gr_item, "setHighlighted"):
                gr_item.setHighlighted(False)

    def _apply_constraint_highlight(self):
        self._clear_constraint_highlight()
        if self.cad is None:
            return

        highlighted = set()
        for item in self.constraints_list.selectedItems():
            data = item.data(Qt.UserRole)
            if data is not None and data[0] == "constraint":
                highlighted.update(data[1].get("objects", []))

        for uuid in highlighted:
            gr_item = self._object_graphics.get(uuid)
            if gr_item is not None and hasattr(gr_item, "setHighlighted"):
                gr_item.setHighlighted(True)

    def add_constraint(self, type, objects, desc=None):
        self.constraints.append({
            'type': type,
            'objects': objects
        })
        self.refresh_constraints_list()

    def _delete_constraint(self, constraint):
        for index, current in enumerate(self.constraints):
            if current is constraint:
                break
        else:
            return

        handle_input(self, input_type="delete_constraint", constaints=constraint)
        del self.constraints[index]

    def delete_selected(self):
        selected_constraints = []
        for item in self.constraints_list.selectedItems():
            data = item.data(Qt.UserRole)
            if data is not None and data[0] == "constraint":
                selected_constraints.append(data[1])

        for constraint in selected_constraints:
            self._delete_constraint(constraint)

        selected = self.cad.scene.grScene.selectedItems()
        uuids = []
        for item in selected:
            if hasattr(item, "uuid") and item.uuid not in uuids:
                uuids.append(item.uuid)

        for item in self.objects_list.selectedItems():
            data = item.data(Qt.UserRole)
            if data is not None and data[0] == "object":
                uuid = getattr(data[1], "uuid", data[1])
                if uuid not in uuids:
                    uuids.append(uuid)

        # каскад: линии, опирающиеся на выделенные точки
        for uuid in list(uuids):
            dot = self.cad.scene.find_dot_by_uuid(uuid)
            if dot is None:
                continue
            for line in self.cad.scene.lines:
                if (line.start_dot is dot or line.end_dot is dot) and line.uuid not in uuids:
                    uuids.append(line.uuid)

        # каскад: ограничения, ссылающиеся на удаляемые сущности
        for constraint in list(self.constraints):
            if set(constraint["objects"]) & set(uuids):
                self._delete_constraint(constraint)

        # сначала линии, затем точки
        for uuid in uuids:
            if self.cad.scene.find_line_by_uuid(uuid):
                self.cad.scene.removeLine(uuid)
        for uuid in uuids:
            if self.cad.scene.find_dot_by_uuid(uuid):
                self.cad.scene.removeDot(uuid)

        for uuid in uuids:
            self.solver.handle_delete(uuid)

        self.refresh_objects_list()
        self.refresh_constraints_list()



    # BUTTONS ACTIONS
    def onButton1Clicked(self):
        handle_input(self, triggered_obj=1)

    def onButton2Clicked(self):
        handle_input(self, triggered_obj=2)

    def onButton3Clicked(self):
        handle_input(self, input_type="constraint_1")

    def onButton5Clicked(self):
        handle_input(self, input_type="constraint_2")

    def onButton6Clicked(self):
        handle_input(self, input_type="constraint_3")

    def onButton7Clicked(self):
        handle_input(self, input_type="constraint_4")

    def onButton8Clicked(self):
        handle_input(self, input_type="constraint_5")

    def onButton9Clicked(self):
        handle_input(self, input_type="constraint_6")

    def onButton10Clicked(self):
        handle_input(self, input_type="constraint_7")

    def onButton11Clicked(self):
        handle_input(self, input_type="constraint_8")

    def onButton12Clicked(self):
        handle_input(self, input_type="constraint_9")

    


    # TEST FUNCTIONAL

    # def test_handle_input(self, triggered_obj):
    #     if triggered_obj:
    #         print(f"Button {triggered_obj} is active")
    #         return (triggered_obj, )
        
    #     # ЗАХАРДКОЖЕНО!!!
    #     if self.coordinates_list:
    #         print(f"Sending {len(self.coordinates_list)} coordinates for drawing")
    #         points_data = [(coord, len(self.coordinates_list) + i) for i, coord in enumerate(self.coordinates_list)]
    #         # coords = self.coordinates_list.copy()
    #         self.coordinates_list.clear()
    #         return (points_data, )
        
    #     return None
        


    # def process_handle_result(self, result):
    #     if not result:
    #         return
        
    #     data = result[0]

    #     if isinstance(data, int):
    #         self.setButtonsActive(data)

    #     elif isinstance(data, list):
    #         self.create_dots_from_coordinates(data)
    #         self.reset_buttons_active()

    #     return
    
    
    def create_dots_from_coordinates(self, coord, uuid):
        if self.cad and self.cad.scene:
                
                x, y = coord[0], coord[1]

                dot = self.cad.scene.find_dot_by_uuid(uuid)
                # тут возможно стоит делать set pos просто
                if dot:
                    # dot.x = x
                    # dot.y = y
                    # self.cad.scene.update_dot_graphics(dot)
                    dot.setPos(x, y)
                    print(f"dot has been updated")
                else:
                    new_dot = self.cad.scene.addDot(Dot(self.cad.scene, uuid=uuid, x=x, y=y))
                    print(f"Created new dot with uuid={uuid}")
                    self.refresh_objects_list()


    def create_line_from_coordinates(self, dots, uuid):
        if self.cad and self.cad.scene:
            dot1 = dots[0]
            dot2 = dots[1]
            line = self.cad.scene.find_line_by_uuid(uuid)

            if line:
                print("already exits")
            else:
                new_line = self.cad.scene.addLine(Line(self.cad.scene, uuid, dot1, dot2))
                self.refresh_objects_list()

    
    def apply_button_style(self, btn, cls):
        btn.setProperty("class", cls)
        btn.style().unpolish(btn)
        btn.style().polish(btn)

    def reset_buttons_active(self):
        self.btn1.setEnabled(True)
        self.btn2.setEnabled(True)
        self.btn3.setEnabled(True)
        self.apply_button_style(self.btn1, "bla")
        self.apply_button_style(self.btn2, "bla")
        self.apply_button_style(self.btn3, "bla")
        self.active_button = None
    

    def setButtonsActive(self, button_id):
        """Закрашивает активную кнопку, остальные - серые"""
        # Все кнопки серые
        # self.btn1.setStyleSheet("background-color: #CCCCCC;")
        # self.btn2.setStyleSheet("background-color: #CCCCCC;")
        # self.btn3.setStyleSheet("background-color: #CCCCCC;")

        # print(f"setting button active %d", button_id)

        self.reset_buttons_active()

        self.btn1.setEnabled(False)
        self.btn2.setEnabled(False)
        self.btn3.setEnabled(False)

        if button_id == 1:
            self.btn1.setEnabled(True)
            self.apply_button_style(self.btn1, "active")
        if button_id == 2:
            self.btn2.setEnabled(True)
            self.apply_button_style(self.btn2, "active")
        if button_id == 3:
            self.btn3.setEnabled(True)
            self.apply_button_style(self.btn3, "active")

        self.active_button = button_id        
        # Активная кнопка зеленая
        # active_button.setStyleSheet("background-color: #4EEA00; color: white;")


