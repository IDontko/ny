/**
 *
 * Created by limengjun on 2016/12/12.
 */

var page = require('webpage').create(),
system=require('system'),
address;
if(system.args.length==1){
    phantom.exit();
}else {
    address=system.args[1];
    page.open(address, function() {
        page.render('screenshot.jpg')
        phantom.exit();
    });
};
