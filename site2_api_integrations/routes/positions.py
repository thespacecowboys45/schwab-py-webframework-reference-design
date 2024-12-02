from flask import Blueprint, render_template, jsonify, g
import services.positions

positions_bp = Blueprint('positions', __name__)

@positions_bp.route('/positions')
def positions():
    return render_template('positions/positions.html', base_template=g.base_template, title="Positions")
