import os
import csv
import zipfile

def create_package(game, session):
    from models import Player, Impression, Engagement, Session as GameSession  # למנוע circular import

    package_dir = os.path.join('packages', game.name)
    os.makedirs(package_dir, exist_ok=True)

    create_csv_file(game, package_dir, 'players.csv', Player, session)
    create_csv_file(game, package_dir, 'impressions.csv', Impression, session)
    create_csv_file(game, package_dir, 'engagements.csv', Engagement, session)
    create_csv_file(game, package_dir, 'sessions.csv', GameSession, session)

    package_path = f'{package_dir}.zip'
    with zipfile.ZipFile(package_path, 'w') as zipf:
        for root, _, files in os.walk(package_dir):
            for file in files:
                full_path = os.path.join(root, file)
                zipf.write(full_path, os.path.relpath(full_path, package_dir))

    return package_path


def create_csv_file(game, package_dir, filename, model, session):
    filepath = os.path.join(package_dir, filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        columns = [column.name for column in model.__table__.columns]
        writer.writerow(columns)
        records = session.query(model).filter_by(game_id=game.id).all()
        for record in records:
            writer.writerow([getattr(record, column) for column in columns])
