import threading

class Controller(object):
    def __init__(self, model, view):
        self._model = model
        self._view = view

        self._view.connect_search_clicked(self.searchClicked)
        self._view.connect('destroy', self._view.quit)
        self._view.connect_home_clicked(self.homeClicked)
        self._view.connect_search_bar_changed(self.barChanged)
    
    
    def main(self):
        self._view.run()
    

    def searchClicked(self, button, *args):
        command_searched = self._view.search_bar.get_text().strip()
        if command_searched == "":
            return # Mostrar error: comando vacío

        if (self._view.state=="Home"):
            self._view.hide_home()
            self._view.show_search()
        
        # Si la vista es la de resultados (o resultado) solamente es necesario 
        # actualizar la vista
        self.search_command(command_searched)


    def homeClicked(self, button, *args):
        if (self._view.state == "Results" or self._view.state=="Result"):
            self._view.hide_search()
            self._view.show_home()
        elif (self._view.state == "Error"):
            self._view.hide_error()
            self._view.show_home()
        else: # state is "Home"
            return
 

    def search_command(self, command_searched):
        thread = threading.Thread(
        	target=self._model.search_command, 
        	args=(command_searched, self.update_search_results)
        )
        thread.daemon = True
        thread.start()
        thread.join()

        
    def barChanged(self, widget, *args):
        enabled =  self._view.search_bar.get_text().strip() == ""
        self._view.update_button(enabled)

    def update_search_results(self, search):
        if (search == ["ConnectionError"] or search == []):
            self._view.hide_search()
            self._view.show_error(search)
           
        else:
            self._view.display_command(search)

