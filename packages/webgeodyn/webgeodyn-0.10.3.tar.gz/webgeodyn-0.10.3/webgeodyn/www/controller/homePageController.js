/**
 * Controller of the home page.
 */
class HomePageController{
    /**
     *
     * @param {MainController} mainController - The main controller of the page
     */
    constructor(mainController) {
        this.mc = mainController;
        console.log("Building HomePageController...");
    }

    documentReady(){
        //Add banner
        let banner = new Banner(
            '#maincontentdiv',
            '<h3 class="ui" style="text-align: center"><a href="https://gricad-gitlab.univ-grenoble-alpes.fr/Geodynamo/pygeodyn">pygeodyn</a> (Python geomagnetic data assimilation package) and <a href="https://gricad-gitlab.univ-grenoble-alpes.fr/Geodynamo/webgeodyn">webgeodyn</a> (visualisation tool deployed on this website) are now available for download !</h3>',
            'info');

        //Add long description
        $('#longDesc').load("view/longDesc.html");

        //Add core flow descriptions
        $.get("view/coreflowDesc.html", function(data){
            $('#maincontentdiv .segment').append(data);
        });
    }
}