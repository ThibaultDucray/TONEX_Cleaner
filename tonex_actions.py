# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# Author: Thibault Ducray
# Date: 2025-12-02
# Description: TONEX_Cleaner

import sqlite3
import re

DB_PATH = "Library.db" 

class TonexActions:
    def prepare_clean_suffixes(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Fetch all preset names from Presets
        cursor.execute("SELECT Tag_PresetName FROM Presets")
        all_names = [row[0] for row in cursor.fetchall()]

        # Group names by base name
        changes = []
        groups = {}
        for name in all_names:
            match = re.match(r"(.*)_(\d{1,3})$", name) # re.match(r"^(.*?)(?:_(\\d+))?$", name)
            if match:
                changes.append(name)
                base, num = match.groups()
                if base not in groups:
                    groups[base] = []
                if num:
                    groups[base].append((name, int(num)))
                else:
                    groups[base].append((name, 0))
        conn.close()
        return changes, groups, all_names
    
    def exec_clean_suffixes(self, groups, all_names):
        changes = []
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        for base, items in groups.items():
            suffixed = [(n, num) for n, num in items if num > 0]

            if suffixed:
                # Delete unsuffixed if exists
                if base in all_names:
                    cursor.execute("DELETE FROM Presets WHERE Tag_PresetName = ?", (base,))
                    cursor.execute("DELETE FROM PresetFolderAssociations WHERE PresetName = ?", (base,))

                # Keep only highest suffix
                latest = max(suffixed, key=lambda x: x[1])[0]
                for n, num in suffixed:
                    if n != latest:
                        cursor.execute("DELETE FROM Presets WHERE Tag_PresetName = ?", (n,))
                        cursor.execute("DELETE FROM PresetFolderAssociations WHERE PresetName = ?", (n,))

                # Rename latest to base
                cursor.execute("UPDATE Presets SET Tag_PresetName = ? WHERE Tag_PresetName = ?", (base, latest))
                cursor.execute("UPDATE PresetFolderAssociations SET PresetName = ? WHERE PresetName = ?", (base, latest))
                changes.append(f"{latest} -> {base}")

        conn.commit()
        conn.close()
        return changes

        

    def get_total_count(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Presets")
        total = cursor.fetchone()[0]
        conn.close()
        return total

    def load_filtered_names(self, filter):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT Tag_PresetName FROM Presets WHERE Tag_PresetName LIKE ?", ('%' + filter + '%',))
        names = [row[0] for row in cursor.fetchall()]
        conn.close()
        return names

    def search_and_replace(self, tag_name, new_name):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Presets WHERE Tag_PresetName = ?", (tag_name,))
        exists = cursor.fetchone()[0]
        if exists == 0:
            conn.close()
            return 1
        cursor.execute("SELECT COUNT(*) FROM Presets WHERE Tag_PresetName = ?", (new_name,))
        new_exists = cursor.fetchone()[0]
        if new_exists > 0:
            conn.close()
            return 2
        else:
            cursor.execute("UPDATE Presets SET Tag_PresetName = ? WHERE Tag_PresetName = ?", (new_name, tag_name))
            cursor.execute("UPDATE PresetFolderAssociations SET PresetName = ? WHERE PresetName = ?", (new_name, tag_name))
            conn.commit()
            conn.close()
            return 0

    def delete_from_name(self, tag_name):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Presets WHERE Tag_PresetName = ?", (tag_name,))
        cursor.execute("DELETE FROM PresetFolderAssociations WHERE PresetName = ?", (tag_name,))
        conn.commit()
        conn.close()
        return 1
