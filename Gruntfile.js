module.exports = function(grunt){
	var js_files = [
    'static/js/jquery-1.9.1.js',
		'static/js/scout.js'
	];
	
	// Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    concat: {
      dist: {
        src: js_files,
        dest: 'static/js/script.js'
      }
    },
    uglify: {
      build: {
        src: 'static/js/script.js',
        dest: 'static/js/min/script.min.js'
      }
    },
    less: {
      all: {
        files: {
          'static/css/style.css': 'static/css/less/scout.less'
        }
      }
    },
    watch: {
      scrips: {
        files: js_files.concat(['static/css/less/*.less']),
        tasks: [ 'less', 'concat', 'uglify'],
        interrupt: true
      }
    }
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Default task(s).
  grunt.registerTask('default', ['less', 'concat', 'uglify']);
}