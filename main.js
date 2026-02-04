function applyFilters() {
    const selectedGroup = document.getElementById('groupSelect').value;
    const maxPH = document.getElementById('phSlider').value;

    const filteredData = allSites.features.filter(feature => {
        const props = feature.properties;
        
        // Condition 1: Category match
        const matchGroup = (selectedGroup === 'all' || props.Extreme_Group === selectedGroup);
        
        // Condition 2: Numeric range (pH)
        // We treat "N/A" as valid unless the user specifically wants to filter it out
        const matchPH = (props.pH === "N/A" || props.pH <= parseFloat(maxPH));

        return matchGroup && matchPH;
    });

    updateMap(filteredData);
}