import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GdkPixbuf
import gettext
import locale
from pathlib import Path

_ = gettext.gettext
N_ = gettext.ngettext

class View(Gtk.Window):

    __gsignals__ = {
        'button-clicked': (GObject.SIGNAL_RUN_FIRST, None, ())
    }
    
    def run(self):
        self.show_all()
        Gtk.main()

    def quit(cls, widget):
        Gtk.main_quit()


    def __init__(self, **kw):
        # Elementos de internacionalización
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        LOCALE_DIR = Path(__file__).parent / "locale"
        gettext.textdomain("cheatsh")
        locale.bindtextdomain("cheatsh", LOCALE_DIR)
        gettext.bindtextdomain("cheatsh", LOCALE_DIR)
        
        
        # Crear la ventana con el título y una altura y anchura predeterminada
        super(View, self).__init__(
            title="cheat.sh",
            default_width = 960,
            default_height = 540
            )
        self.set_icon_from_file('media/icon.png')

        # Creamos los elementos básicos de la vista, que se compartirán
        self.HomePage = Gtk.VBox(
            orientation = Gtk.Orientation.VERTICAL,
            homogeneous = False,
            spacing = 12,
            margin_top = 90,
            margin_end = 24,
            margin_bottom = 24,
            margin_start = 24
        )
        
        self.hbox = Gtk.HBox(
            halign = Gtk.Align.CENTER,
            hexpand = True,
            homogeneous = False
        )

        # Mostrar la imagen central
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename = "media/cheatshmono.png", 
            width = 600, 
            height = 208, 
            preserve_aspect_ratio =True
        )

        self.logo = Gtk.Image(
            pixbuf = self.pixbuf
        )

        # Barra y botón de búsqueda
        self.search_bar = Gtk.SearchEntry(
            halign = Gtk.Align.CENTER,
            placeholder_text = _("Search for commands..."),
            activates_default = True
        )

        self.search_bar.set_size_request(350, 15)
        self.search_bar.set_activates_default(True)
       
        self.search_button = Gtk.Button(
            label = _("Search"),
            halign = Gtk.Align.CENTER
        )
        self.search_button.set_sensitive(False)
        
        # Botón a la homePage
        self.home_button = Gtk.Button(
            label = "<",
            halign = Gtk.Align.CENTER
        )

        # La vista de resultado será una ListStore, cuyos resultados
        # estarán dispuestos en un grid. Todo esto estará a su vez
        # detro de una box junto a la barra de búsqueda
        
        self.ResultPage = Gtk.VBox(
            orientation = Gtk.Orientation.VERTICAL,
            homogeneous = False,
            spacing = 12,
            margin_top = 24,
            margin_end = 24,
            margin_bottom = 24,
            margin_start = 24
        )

        self.results_model = []

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)

        self.results_list = Gtk.ListStore(str, str)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)

        #Añadida variable state para saber la vista actual
        self.state = "None"

        # La vista por defecto será la de homePage
        self.show_home()
        
        # La pantalla de error tendrá una imagen y un botón para volver atrás
        self.ErrorPage = Gtk.VBox(
            orientation = Gtk.Orientation.VERTICAL,
            homogeneous = False,
            spacing = 12,
            margin_top = 90,
            margin_end = 24,
            margin_bottom = 24,
            margin_start = 24
        )
        
        self.error_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename = "media/error.png", 
            width = 300, 
            height = 300, 
            preserve_aspect_ratio =True
        )
        
        self.error_img = Gtk.Image(
            pixbuf = self.error_pixbuf
        )
        
        self.error_button = Gtk.Button(
            label = _("Home"),
            halign = Gtk.Align.CENTER
        )

        self.error_label = Gtk.Label()
        self.error_description = Gtk.Label()
        self.error_label.set_markup(_("<big><b>AN ERROR HAS OCCURRED</b></big>"))
        #self.error_label.set_markup("<big><b>"
        #        "OOPSIE WOOPSIE!! Uwu We made a fucky wucky!! "
        #        "A wittle fucko boingo! The code monkeys at our "
        #        "headquarters are working VEWY HAWD to fix this!"
        #        "</b></big>")
        self.error_label.set_line_wrap(True)
        self.error_label.set_justify(Gtk.Justification.FILL)

    # Construir la vista Home
    def show_home(self):
        self.add(self.HomePage)
        self.resize(960,540)
        self.HomePage.pack_start(self.logo, False, False, 10)
        self.HomePage.pack_start(self.hbox, False, False, 10)
        
        # Si es la primera vez que se crea la vista, es necesario añadir 
        # la barra y el botón a la hbox
        if self.state == "None":
            self.hbox.pack_start(self.search_bar, False, False, 5)
            self.hbox.pack_start(self.search_button,False, False, 5)
        else:
            self.search_bar.set_text("")
        self.state = "Home"
    
    def hide_home(self):
        self.remove(self.HomePage)
        self.HomePage.remove(self.logo)
        self.HomePage.remove(self.hbox)
       
        
    # Error en la búsqueda
    def show_error(self, search):
        self.add(self.ErrorPage)
        self.ErrorPage.pack_start(self.error_img, False, False, 10)
        self.ErrorPage.pack_start(self.error_label, False, False, 10)

        if (search == ["ConnectionError"]):
            self.error_description.set_text(_("Check your Internet connection."))
        elif (search == []):
            self.error_description.set_text(_("The command you are looking for does not exist."))
        else:
            self.error_description.set_text(_("There's been a kind of mistake."))

        self.ErrorPage.pack_start(self.error_description, False, False, 10)
        self.ErrorPage.pack_start(self.error_button, False, False, 10)
        self.show_all()
        self.state = "Error"
    

    def hide_error(self):
        self.remove(self.ErrorPage)
        self.ErrorPage.remove(self.error_img)
        self.ErrorPage.remove(self.error_label)
        self.ErrorPage.remove(self.error_description)
        self.ErrorPage.remove(self.error_button)
    
    # Construir la tabla de resultados y mostrarla
    def display_command(self, result):
        if (self.state == "Result"):
            self.ResultPage.remove(self.grid)
            self.scrollable_treelist.remove(self.treeview)

        # Si la lista tenía otros resultados, se borran
        self.results_list.clear()   
        #result es None en caso de un error de conexión, por ejemplo
        for command_ref in result:
            self.results_list.append(list(command_ref))

        self.treeview = Gtk.TreeView(model=self.results_list)

        # Indicar las columnas que tendrá la tabla
        for i, column_title in enumerate(
            [_("Name"), _("Description")]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        self.scrollable_treelist.add(self.treeview)
        self.ResultPage.pack_end(self.grid, True, True, 0)
        self.show_all()
        self.state = "Result"


    # Construir la vista de resultado
    def show_search(self):
        self.add(self.ResultPage)
        self.ResultPage.pack_start(self.hbox, False, False, 0)
        # Añadir el botón para volver atrás y colocarlo el primero
        self.hbox.pack_start(self.home_button, False, False, 5) 
        self.hbox.reorder_child(self.home_button, 0)
        self.show_all()
        self.state = "Results"

    def hide_search(self):
        self.hbox.remove(self.home_button)
        self.ResultPage.remove(self.hbox)
        if (self.state == "Result"):
            self.ResultPage.remove(self.grid)
            self.scrollable_treelist.remove(self.treeview)
        self.remove(self.ResultPage)

    def update_button(self, enabled, *args):
        if enabled:
            self.search_button.set_sensitive(False)
        else:
            self.search_button.set_sensitive(True)


    # Conectar los botones y la barra de búsqueda a las funciones del controller
    def connect_search_clicked(self, fun):
        self.search_button.connect("clicked", fun)
        self.search_bar.connect("activate", fun)
    
    def connect_home_clicked(self, fun):
        self.home_button.connect("clicked", fun)
        self.error_button.connect("clicked", fun)

    def connect_search_bar_changed(self, fun):
        self.search_bar.connect("changed",fun)
